import argparse
import pandas as pd


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--model_predict_file', type=str, default='../server/metadata/guardrail_classification.csv',
                    help='input model prediction file with path')
parser.add_argument('--labeled_file', type=str, default='../server/metadata/training_Image_guardrail_yn.csv',
                    help='input labelled file with path to compare prediction with')
parser.add_argument('--server_url', type=str, default='http://localhost',
                    help='the server url to create html file for')
parser.add_argument('--output_html_file', type=str, default='../server/templates/show_misclassified_images.html',
                    help='the server url to create html file for')
args = parser.parse_args()
input_pred_file = args.model_predict_file
labeled_file = args.labeled_file
server_url = args.server_url
output_html_file = args.output_html_file

html_str_head = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Show images misclassified as containing guardrails</title>
</head>
<body>    
"""
html_str_tail = """
</body>
</html>
"""

img_str = """
<div style="display: flex;">
    <img src='/get_image_by_name/{image_base_name}5.jpg' style="float:left;width:33.33%;"/>
    <img src='/get_image_by_name/{image_base_name}1.jpg' style="float:left;width:33.33%;"/>
    <img src='/get_image_by_name/{image_base_name}2.jpg' style="float:left;width:33.33%;"/>
</div>
<p>Prediction probability: {probability}</p>
"""

pred_df = pd.read_csv(input_pred_file, header=0, index_col='MAPPED_IMAGE', dtype={'MAPPED_IMAGE': 'str',
                                                                                  'Probability': 'float'})

pred_df.dropna(inplace=True)

label_df = pd.read_csv(labeled_file, header=0, index_col='MAPPED_IMAGE', dtype=str, usecols=["MAPPED_IMAGE",
                                                                                                   "GUARDRAIL_YN"])
concat_df = pd.concat([pred_df, label_df], axis=1, sort=False)

inconsist_df_n = concat_df[(concat_df['Probability'] <= 0.1) & (concat_df['GUARDRAIL_YN']=='Y')]
print(inconsist_df_n.shape)
img_str_list = []
inconsist_df_n.apply(lambda row: img_str_list.append(img_str.format(image_base_name=row.name,
                                                                    probability=row['Probability'])), axis=1)
html_img_str = '\n'.join(img_str_list)
html_str = f"{html_str_head}\n{html_img_str}\n{html_str_tail}"
with open(output_html_file, 'w') as file:
    file.write(html_str)
