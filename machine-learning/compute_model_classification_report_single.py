import pandas as pd
import argparse
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


def create_single_data(base_image_name, left_view, front_view, right_view, single_data_list):
    single_data_list.append([f'{base_image_name}5', 'True' if left_view == 'p' else 'False'])
    single_data_list.append([f'{base_image_name}1', 'True' if front_view == 'p' else 'False'])
    single_data_list.append([f'{base_image_name}2', 'True' if right_view == 'p' else 'False'])
    return


def create_single_data_frame(joined_df):
    single_image_data_list = []
    joined_df.apply(lambda row: create_single_data(row.name, row.LeftView, row.FrontView,
                                                   row.RightView, single_image_data_list),
                    axis=1)
    return pd.DataFrame(single_image_data_list, columns=['Image', 'Presence'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--label_file', type=str,
                        #default='../server/metadata/holdout_test/user_annoted_image_info_for_holdout.csv',
                        #default='../server/metadata/holdout_test/user_annoted_balanced_image_info.txt',
                        #default='../server/metadata/pole/holdout_test_user_annots_balanced_edited.csv',
                        default='../server/metadata/pole/holdout_test_user_annots_edited.csv',
                        help='labelled guardrail data obtained from guardrail survey data')
    parser.add_argument('--predict_label_file', type=str,
                        default='../server/metadata/pole/round2/model_predict_test_unbalanced.csv',
                        help='Model prediction on the single images')
    parser.add_argument('--threshold', type=float, default=0.64, help='threshold to separate two classes')
    parser.add_argument('--single_metrics', type=bool, default=False,
                        help='if True, assess metrics for single image; otherwise, assess metrics for joined image')

    args = parser.parse_args()
    label_file = args.label_file
    predict_label_file = args.predict_label_file
    single_metrics = args.single_metrics
    threshold = args.threshold

    label_df = pd.read_csv(label_file, header=0, index_col='Image', dtype=str)
    label_df.index = label_df.index.str.split('/').str[-1]
    label_df.index = label_df.index.str.replace('.jpg', '')

    single_df = pd.read_csv(predict_label_file, header=0, index_col=None, dtype={'MAPPED_IMAGE': 'str',
                                                                                 'ROUND_PREDICT': 'float'})
    single_df.MAPPED_IMAGE = single_df.MAPPED_IMAGE.str.split('/').str[-1]
    single_df.MAPPED_IMAGE = single_df.MAPPED_IMAGE.str.replace('.jpg', '')
    if single_metrics:
        single_label_df = create_single_data_frame(label_df)
        single_df = single_df[single_df.MAPPED_IMAGE.isin(single_label_df.Image)]
        single_label_df.set_index('Image', inplace=True)
        single_df.set_index('MAPPED_IMAGE', inplace=True)
        concat_df = pd.concat([single_label_df, single_df], axis=1)
        concat_df['ROUND_PREDICT_SINGLE'] = concat_df.apply(lambda row: 1 if row.ROUND_PREDICT >= threshold else 0, axis=1)
    else:
        single_df['GROUP'] = single_df.MAPPED_IMAGE.str[:-1]
        single_df['ROUND_PREDICT_GROUP'] = single_df.apply(lambda row: 1 if row.ROUND_PREDICT >= threshold else 0, axis=1)
        single_df.drop(columns=['ROUND_PREDICT'], inplace=True)
        single_df = single_df.groupby(by=['GROUP']).sum()
        single_df = single_df.reset_index()
        print('single_df size before filtering:', single_df.shape)
        single_df = single_df[single_df.GROUP.isin(label_df.index)]
        single_df = single_df.set_index('GROUP')
        print('single_df size after filtering:', single_df.shape)
        concat_df = pd.concat([single_df, label_df], axis=1)
        concat_df.rename(columns={'index': 'MAPPED_IMAGE'}, inplace=True)
        concat_df['ROUND_PREDICT_SINGLE'] = concat_df.apply(lambda row: 1 if row.ROUND_PREDICT_GROUP > 0 else 0, axis=1)

    concat_df['Presence'] = concat_df.Presence.apply(lambda row: 0 if row == 'False' else 1)

    print('Classification Report')
    print(classification_report(concat_df['Presence'], concat_df['ROUND_PREDICT_SINGLE']))
    print('Confusion Matrix')
    cm = confusion_matrix(concat_df['Presence'], concat_df['ROUND_PREDICT_SINGLE'])
    print(cm)
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax, cmap='Blues', fmt="d")
    ax.set_title('Confusion Matrix')
    ax.set_xlabel('Predicted Labels')
    ax.set_ylabel('True Labels')
    ax.xaxis.set_ticklabels(['Not Guardrail', 'Guardrail'])
    ax.yaxis.set_ticklabels(['Not Guardrail', 'guardrail'])
    plt.show()
