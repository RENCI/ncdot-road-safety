import argparse
import pandas as pd


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_guardrail_file', type=str, default='../server/metadata/training_image_subset_10000.csv',
                    help='input guardrail label file with path')
parser.add_argument('--output_html_file', type=str, default='../server/templates/show_guardrail_images.html',
                    help='the output html file for looking at guardrail images')

args = parser.parse_args()
input_guardrail_file = args.input_guardrail_file
output_html_file = args.output_html_file

df = pd.read_csv(input_guardrail_file, header=0, dtype=str, usecols=['MAPPED_IMAGE', 'GUARDRAIL_YN'])
df = df[df.GUARDRAIL_YN == 'Y']
print(df.shape)
df = df.sample(n=100, random_state=1)
print(df.shape)
html_str_head = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Show guardrail images used for training the model classifier</title>
</head>
<body>    
"""
html_str_tail = """
</body>
</html>
"""

img_str = """
<div style="display: flex;">
    <img src='/get_original_image_by_name/{image_base_name}5.jpg' style="float:left;width:33.33%;"/>
    <img src='/get_original_image_by_name/{image_base_name}1.jpg' style="float:left;width:33.33%;"/>
    <img src='/get_original_image_by_name/{image_base_name}2.jpg' style="float:left;width:33.33%;"/>
</div>
<p>Image base name: {image_base_name}</p>
"""
img_str_list = []
df.apply(lambda row: img_str_list.append(img_str.format(image_base_name=row['MAPPED_IMAGE'])), axis=1)
html_img_str = '\n'.join(img_str_list)
html_str = f"{html_str_head}\n{html_img_str}\n{html_str_tail}"
with open(output_html_file, 'w') as file:
    file.write(html_str)
