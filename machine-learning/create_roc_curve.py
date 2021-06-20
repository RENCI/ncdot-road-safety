import pandas as pd
import argparse
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
from utils import create_single_data_frame


# model_predict_file_list = [
#     '../server/metadata/model_predict_test_base.csv',
#     '../server/metadata/model_predict_test_round1.csv',
#     '../server/metadata/model_predict_test_round2.csv',
#     '../server/metadata/model_predict_test_round3.csv',
#     '../server/metadata/model_predict_test_round4.csv',
#     '../server/metadata/model_predict_test_round5.csv'
# ]

model_predict_file_list = [
    '../server/metadata/pole/round1/model_predict_test.csv',
    '../server/metadata/pole/round2/model_predict_test_unbalanced.csv',
    '../server/metadata/pole/round3/model_predict_test_i_as_a.csv'
]


def read_predict_file(filename, rename_cols=None):
    pred_df = pd.read_csv(filename, header=0, index_col=False,
                          dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                          usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
    pred_df['MAPPED_IMAGE'] = pred_df['MAPPED_IMAGE'].str.split('/').str[-1]
    pred_df['MAPPED_IMAGE'] = pred_df['MAPPED_IMAGE'].str.replace('.jpg', '')
    if rename_cols is not None:
        pred_df.rename(columns=rename_cols, inplace=True)
    pred_df = pred_df[pred_df.MAPPED_IMAGE.isin(df_in.index)]
    pred_df = pred_df.set_index('MAPPED_IMAGE')
    return pred_df


def draw_roc_curve(y_true, y_score):
    fpr, tpr, thresholds = roc_curve(y_true, y_score, pos_label=1)
    plt.plot(fpr, tpr, linewidth=2)
    return round(roc_auc_score(y_true, y_score), 3)


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    #default='../server/metadata/holdout_test/user_annoted_image_info_for_holdout.csv',
                    #default='../server/metadata/holdout_test/user_annoted_balanced_image_info.txt',
                    #default='../server/metadata/pole/holdout_test_user_annots_balanced_edited.csv',
                    default='../server/metadata/pole/holdout_test_user_annots_edited.csv',
                    help='input file with path to create roc curve from')
parser.add_argument('--curve_title', type=str, default='ROC Curve', help='ROC curve title')
parser.add_argument('--single_image', type=bool, default=True,
                    help='if True, create roc curve for single imagge rather than for joined image')


args = parser.parse_args()
input_file = args.input_file
curve_title = args.curve_title
single_image = args.single_image

df_in = pd.read_csv(input_file, header=0, index_col=False, dtype=str)
df_in['Image'] = df_in['Image'].str.split('/').str[-1]
df_in['Image'] = df_in['Image'].str.replace('.jpg', '')
df_in.set_index('Image', inplace=True)
if single_image:
    df_in = create_single_data_frame(df_in)
    df_in.set_index('Image', inplace=True)
df_al_list = []
for num, predict_file in enumerate(model_predict_file_list):
    if num == 0:
        df_al_list.append(read_predict_file(predict_file))
    else:
        df_al_list.append(read_predict_file(predict_file,
                                            rename_cols={'ROUND_PREDICT': f'ROUND_PREDICT{num}'}))

df_al_list.insert(0, df_in)
df_all = pd.concat(df_al_list, axis=1)
df_all = df_all.reset_index()
df_all['Presence'] = df_all.Presence.apply(lambda row: 0 if row == 'False' else 1)
print(df_all.shape)

plt.title(curve_title)
plt.ylabel('True Positive Rate (Recall)')
plt.xlabel('False Positive Rate')

legend_score_strs = []
for num, _ in enumerate(model_predict_file_list):
    if num == 0:
        score = draw_roc_curve(df_all['Presence'], df_all['ROUND_PREDICT'])
        legend_score_strs.append(f'Round{num+1} model (AUC: {score})')
    else:
        score = draw_roc_curve(df_all['Presence'], df_all[f'ROUND_PREDICT{num}'])
        legend_score_strs.append(f'Round{num+1} model (AUC: {score})')

plt.legend(legend_score_strs, loc='lower right')
plt.plot([0, 1], [0, 1], 'k--')
plt.show()
