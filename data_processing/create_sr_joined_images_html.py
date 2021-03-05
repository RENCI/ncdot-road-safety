import argparse
import pandas as pd


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str, default='../server/metadata/model_2lane_predict_d4_with_manual_labels.csv',
                    help='input image file with model prediction')
parser.add_argument('--output_html_file', type=str, default='../server/templates/model_2lane_d4_subset.html',
                    help='the output html file for looking at images')

args = parser.parse_args()
input_file = args.input_file
output_html_file = args.output_html_file

df = pd.read_csv(input_file, header=0, dtype=str)
df['index'] = df['index'].str.replace('.jpg', '')
print(df.shape)
html_str_head = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Show d4 test holdout images with baseline model prediction info</title>
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
<p>Image base name: {image_base_name}, annotation: {annotation}, prediction: {prob} {WRONG}</p>
"""
img_str_list = []
df.apply(lambda row: img_str_list.append(img_str.format(image_base_name=row['index'],
                                                        annotation=row['Presence'],
                                                        prob=row['ROUND_PREDICT'],
                                                        WRONG="<b>WRONG</b>" if row['WRONG'] == 'Red' else '')), axis=1)
html_img_str = '\n'.join(img_str_list)
html_str = f"{html_str_head}\n{html_img_str}\n{html_str_tail}"
with open(output_html_file, 'w') as file:
    file.write(html_str)
