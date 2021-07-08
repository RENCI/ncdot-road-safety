import pandas as pd
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file', type=str,
                        default='../server/metadata/predict/pole/deliverable/pole_model_predict_d4.csv',
                        help='input prediction file with route id and mile post')

    args = parser.parse_args()
    input_file = args.input_file

    input_df = pd.read_csv(input_file, header=0, index_col=None, usecols=['MAPPED_IMAGE', 'ROUTEID', 'MILE_POST',
                                                                          'PRESENCE'])
    input_df = input_df.sort_values(by=['ROUTEID', 'MILE_POST'])
    total = len(input_df)
    yes_total = len(input_df[input_df.PRESENCE == True])
    route_ids = input_df.ROUTEID.unique()
    total_miles = 0
    total_yes_miles = 0
    for rid in route_ids:
        route_df = input_df[input_df.ROUTEID==rid]
        # get mile post difference between 2 consecutive rows
        diff_df = route_df.drop(columns=['PRESENCE', 'ROUTEID']).diff()
        total_miles += diff_df.MILE_POST.sum()
        route_yes_df = route_df[route_df.PRESENCE==True].drop(columns=['PRESENCE', 'ROUTEID'])
        yes_diff_df = route_yes_df.diff()
        negative_df = yes_diff_df[yes_diff_df.MILE_POST < 0]
        if not negative_df.empty:
            print('route id:', rid)
            print(negative_df)
        yes_diff_df = yes_diff_df[yes_diff_df.MILE_POST < 0.03]
        total_yes_miles += yes_diff_df.MILE_POST.sum()

    print('guardrail image percentage: ', yes_total/total)
    print('Total miles: ', total_miles, ', guardrail miles: ', total_yes_miles, ', guardrail mile percentage: ',
          total_yes_miles/total_miles)
