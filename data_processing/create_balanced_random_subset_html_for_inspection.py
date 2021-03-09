import argparse
import pandas as pd


def create_html_file_for_inspection(input_df, output_file_name, two_models=True):
    html_str_head = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Show randomly selected 100 secondary road images used for assessing the model classifier</title>
    </head>
    <body>    
    """
    html_str_tail = """
    </body>
    </html>
    """

    img_str = """
    <div style='display: flex;'>
        <img src='/get_image_by_name/{image_base_name}5.jpg' style="float:left;width:33.33%;"/>
        <img src='/get_image_by_name/{image_base_name}1.jpg' style="float:left;width:33.33%;"/>
        <img src='/get_image_by_name/{image_base_name}2.jpg' style="float:left;width:33.33%;"/>        
    </div>
    <p>Image base name: {image_base_name}, 2 lane model prediction: {prob2}{WRONG} 
    """
    if two_models:
        img_str += ", updated model prediction: {prob}{WRONG2}</p>"
    else:
        img_str += "</p>"

    img_str_list = []
    if two_models:
        input_df.apply(lambda row: img_str_list.append(img_str.format(image_base_name=row['MAPPED_IMAGE'],
                                                                      prob2=row['ROUND_PREDICT_2'],
                                                                      WRONG="<b>WRONG</b>" if row['WRONG']==1 else '',
                                                                      prob=row['ROUND_PREDICT'],
                                                                      WRONG2="<b>WRONG</b>" if row['WRONG2']==1 else '')),
                       axis=1)
    else:
        input_df.apply(lambda row: img_str_list.append(img_str.format(image_base_name=row['MAPPED_IMAGE'],
                                                                      prob2=row['ROUND_PREDICT_2'],
                                                                      WRONG="<b>WRONG</b>" if row['WRONG']==1 else '')),
                       axis=1)
    html_img_str = '\n'.join(img_str_list)
    html_str = f"{html_str_head}\n{html_img_str}\n{html_str_tail}"
    with open(output_file_name, 'w') as file:
        file.write(html_str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--input_file', type=str,
                        default='../server/metadata/d4_subset_with_manual_inspection_300_new.csv',
                        help='input image file with model prediction')
    parser.add_argument('--output_html_file', type=str, default='../server/templates/model_2lane_d4_subset_old.html',
                        help='the output html file for looking at images')

    args = parser.parse_args()
    input_file = args.input_file
    output_html_file = args.output_html_file

    df = pd.read_csv(input_file, header=0, usecols=['MAPPED_IMAGE', 'MANUAL_YN', 'ROUND_PREDICT_2', 'ROUND_PREDICT'],
                     dtype={'MAPPED_IMAGE': str, 'MANUAL_YN': str, 'ROUND_PREDICT_2': float, 'ROUND_PREDICT': float})
    df['WRONG'] = df.apply(lambda row: 1 if ((row['ROUND_PREDICT_2'] < 0.5 and row['MANUAL_YN'] == 'Y') or
                                             (row['ROUND_PREDICT_2'] >= 0.5 and row['MANUAL_YN'] == 'N')) else 0,
                           axis=1)
    df['WRONG2'] = df.apply(lambda row: 1 if ((row['ROUND_PREDICT'] < 0.5 and row['MANUAL_YN'] == 'Y') or
                                             (row['ROUND_PREDICT'] >= 0.5 and row['MANUAL_YN'] == 'N')) else 0,
                            axis=1)
    print(df.shape)
    create_html_file_for_inspection(df, output_html_file)
    print('Done')
