import sys
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print('Two input parameters, input file from model prediction and input file from guardrail ingestion, '
              'are needed to run the script')
        exit(1)

    input_pred_file = sys.argv[1]
    input_ingest_file = sys.argv[2]
    pred_df = pd.read_csv(input_pred_file, header=0, index_col='MAPPED_IMAGE', dtype={'MAPPED_IMAGE': 'str',
                                                                                      'Probability': 'float'})

    pred_df.dropna(inplace=True)

    ingest_df = pd.read_csv(input_ingest_file, header=0, index_col='MAPPED_IMAGE', dtype=str, usecols=["MAPPED_IMAGE",
                                                                                                       "GUARDRAIL_YN"])
    concat_df = pd.concat([pred_df, ingest_df], axis=1, sort=False)
    inconsist_df_y = concat_df[(concat_df['Probability']>=0.5) & (concat_df['GUARDRAIL_YN']=='N')]
    print(inconsist_df_y.shape, inconsist_df_y)
    inconsist_df_n = concat_df[(concat_df['Probability'] < 0.5) & (concat_df['GUARDRAIL_YN']=='Y')]
    print(inconsist_df_n.shape, inconsist_df_n)
