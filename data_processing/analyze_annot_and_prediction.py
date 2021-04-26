import pandas as pd
import argparse
from create_uncertainty_scores import get_pred_dataframe_from_csv


def get_division_count(input_df, div_str):
    return len(input_df[input_df.DIVISION==div_str])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--label_file', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round4/annot_data/'
                                'user_annots.txt',
                        help='manually labelled data from AL')
    parser.add_argument('--input_file_d4', type=str,
                            default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/predict/predict_d4.csv',
                            help='input prediction file for mapped images')
    parser.add_argument('--input_file_d8', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/predict/predict_d8.csv',
                        help='input prediction file for mapped images')
    parser.add_argument('--input_file_d13', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/predict/predict_d13.csv',
                        help='input prediction file for mapped images')
    parser.add_argument('--input_file_d14', type=str,
                        default='/projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round3/predict/predict_d14.csv',
                        help='input prediction file for mapped images')

    args = parser.parse_args()
    label_file = args.label_file
    input_file_d4 = args.input_file_d4
    input_file_d8 = args.input_file_d8
    input_file_d13 = args.input_file_d13
    input_file_d14 = args.input_file_d14

    predict_file_list = {
        input_file_d4, input_file_d8, input_file_d13, input_file_d14
    }

    df_annot = pd.read_csv(label_file, header=0, index_col=False, dtype=str, usecols=['Image', 'Presence'])
    df_annot = df_annot.drop_duplicates(subset=['Image'])
    print('annotation file shape: ', df_annot.shape)
    df_annot = df_annot.set_index('Image')
    df_annot.index = df_annot.index.str.replace('.jpg', '')
    df_annot.index = df_annot.index.str.split('/').str[-1]

    df_predict_list = []
    for predict_file in predict_file_list:
        df_predict_list.append(get_pred_dataframe_from_csv(predict_file))
    df_predict = pd.concat[df_predict_list]
    df_predict = df_predict.reset_index()
    df_predict = df_predict[df_predict.MAPPED_IMAGE.isin(df_annot.index)]
    df_predict = df_predict.set_index('MAPPED_IMAGE')
    df = pd.concat([df_predict, df_annot], axis=1)
    df['WRONG'] = df.apply(lambda row: 1 if ((row['ROUND_PREDICT'] < 0.5 and row['Presence']=='True')
                                             or (row['ROUND_PREDICT'] >= 0.5 and row['Presence']=='False')) else 0, axis=1)
    print('Total annotated image df shape', df.shape)
    wrong_df = df[df['WRONG']==1]
    wrong_cnt =len(wrong_df)
    print('caught total FPs and FNs:', wrong_cnt, '(', wrong_cnt/len(df) + ')',
          ' (d4:', get_division_count(wrong_df, 'd04'), ', d8:', get_division_count(wrong_df, 'd08'),
          ', d13:', get_division_count(wrong_df, 'd13'), ', d14:', get_division_count(wrong_df, 'd14'), ')')
    fp_df = df[(df['WRONG']==1) & (df['Presence']=='False')]
    fn_df = df[(df['WRONG']==1) & (df['Presence']=='True')]
    print('caught total FPs:', len(fp_df), ' (d4:', get_division_count(fp_df, 'd04'),
          ', d8:', get_division_count(fp_df, 'd08'),
          ', d13:', get_division_count(fp_df, 'd13'), ', d14:', get_division_count(fp_df, 'd14'), ')')
    print('caught total FNs:', len(fn_df), ' (d4:', get_division_count(fn_df, 'd04'),
          ', d8:', get_division_count(fn_df, 'd08'),
          ', d13:', get_division_count(fn_df, 'd13'), ', d14:', get_division_count(fn_df, 'd14'), ')')
