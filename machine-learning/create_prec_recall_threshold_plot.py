import pandas as pd
import argparse
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from utils import create_single_data_frame


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str,
                    #default='../server/metadata/holdout_test/user_annoted_image_info_for_holdout_d13_d14.txt',
                    #default='../server/metadata/pole/holdout_test_user_annots_balanced_edited.csv',
                    default='../server/metadata/pole/holdout_test_user_annots_edited.csv',
                    help='input file with path to create roc curve from')
parser.add_argument('--model_predict_file', type=str,
                    #default='../server/metadata/model_predict_test_round3.csv',
                    default='../server/metadata/pole/round2/model_predict_test_unbalanced.csv',
                    help='the active learning model prediction file')
parser.add_argument('--single_image', type=bool, default=True,
                    help='if True, create roc curve for single imagge rather than for joined image')

args = parser.parse_args()
input_file = args.input_file
model_predict_file = args.model_predict_file
single_image = args.single_image

df_in = pd.read_csv(input_file, header=0, index_col=False, dtype=str)
df_in['Image'] = df_in['Image'].str.split('/').str[-1]
df_in['Image'] = df_in['Image'].str.replace('.jpg', '')
df_in.set_index('Image', inplace=True)
if single_image:
    df_in = create_single_data_frame(df_in)
    df_in.set_index('Image', inplace=True)

df_al = pd.read_csv(model_predict_file, header=0, index_col=False,
                    dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float},
                    usecols=['MAPPED_IMAGE', 'ROUND_PREDICT'])
df_al['MAPPED_IMAGE'] = df_al['MAPPED_IMAGE'].str.split('/').str[-1]
df_al['MAPPED_IMAGE'] = df_al['MAPPED_IMAGE'].str.replace('.jpg', '')
df_al = df_al[df_al.MAPPED_IMAGE.isin(df_in.index)]
df_al = df_al.set_index('MAPPED_IMAGE')
df = pd.concat([df_in, df_al], axis=1)
df = df.reset_index()
df['Presence'] = df.Presence.apply(lambda row: 0 if row == 'False' else 1)
print(df.shape)

precision, recall, thresholds = precision_recall_curve(df['Presence'].to_numpy(), df['ROUND_PREDICT'].to_numpy(), pos_label=1)
plt.plot(thresholds, precision[:-1], 'b--', linewidth=2, label='Precision')
plt.plot(thresholds, recall[:-1], 'g-', linewidth=2, label='Recall')
plt.xlabel('Threshold')
plt.legend()
plt.grid(True)
plt.show()
