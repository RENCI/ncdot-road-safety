import pandas as pd
import argparse
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--label_file', type=str,
                    #default='../server/metadata/holdout_test/user_annoted_image_info_for_holdout.csv',
                    default='../server/metadata/holdout_test/user_annoted_balanced_image_info.txt',
                    help='labelled guardrail data obtained from guardrail survey data')
parser.add_argument('--predict_label_file', type=str,
                    default='../server/metadata/round5/single/model_predict_test_single.csv',
                    help='Model prediction on the single images')

args = parser.parse_args()
label_file = args.label_file
predict_label_file = args.predict_label_file

label_df = pd.read_csv(label_file, header=0, index_col='Image', dtype=str)
label_df.index = label_df.index.str.split('/').str[-1]
label_df.index = label_df.index.str.replace('.jpg', '')

single_df = pd.read_csv(predict_label_file, header=0, index_col=None, dtype={'MAPPED_IMAGE': 'str',
                                                                             'ROUND_PREDICT': 'float'})
single_df.MAPPED_IMAGE = single_df.MAPPED_IMAGE.str.split('/').str[-1]
single_df.MAPPED_IMAGE = single_df.MAPPED_IMAGE.str.replace('.jpg', '')
single_df['GROUP'] = single_df.MAPPED_IMAGE.str[:-1]
single_df['ROUND_PREDICT_GROUP'] = single_df.apply(lambda row: 1 if row.ROUND_PREDICT>=0.5 else 0, axis=1)
single_df.drop(columns=['ROUND_PREDICT'], inplace=True)
single_df = single_df.groupby(by=['GROUP']).sum()
single_df = single_df.reset_index()
single_df = single_df[single_df.GROUP.isin(label_df.index)]
single_df = single_df.set_index('GROUP')

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
