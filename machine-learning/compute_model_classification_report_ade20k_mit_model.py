import pandas as pd
import argparse
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--label_file', type=str,
                    default='../server/metadata/pole/holdout_test_user_annots_edited.csv',
                    help='labelled holdout test data for pole')
parser.add_argument('--predict_label_file', type=str,
                    default='../server/metadata/pole/holdout_predictions.csv',
                    help='Model prediction on the single images')

args = parser.parse_args()
label_file = args.label_file
predict_label_file = args.predict_label_file

label_df = pd.read_csv(label_file, header=0, index_col='Image', dtype=str)
label_df.index = label_df.index.str.split('/').str[-1]
label_df.index = label_df.index.str.replace('.jpg', '')

predict_df = pd.read_csv(predict_label_file, header=0, index_col=None, dtype=str)
predict_df = predict_df[predict_df.MAPPED_IMAGE.isin(label_df.index)]
predict_df = predict_df.set_index('MAPPED_IMAGE')

concat_df = pd.concat([predict_df, label_df], axis=1)
concat_df.rename(columns={'index': 'MAPPED_IMAGE'}, inplace=True)
concat_df['POLES_ALL'] = concat_df.POLES_ALL.apply(lambda row: 0 if row == 'False' else 1)
concat_df['Presence'] = concat_df.Presence.apply(lambda row: 0 if row == 'False' else 1)

print('Classification Report')
print(classification_report(concat_df['Presence'], concat_df['POLES_ALL']))
print('Confusion Matrix')
cm = confusion_matrix(concat_df['Presence'], concat_df['POLES_ALL'])
print(cm)
ax = plt.subplot()
sns.heatmap(cm, annot=True, ax=ax, cmap='Blues', fmt="d")
ax.set_title('Confusion Matrix')
ax.set_xlabel('Predicted Labels')
ax.set_ylabel('True Labels')
ax.xaxis.set_ticklabels(['Not Pole', 'Pole'])
ax.yaxis.set_ticklabels(['Not Pole', 'Pole'])
plt.show()
