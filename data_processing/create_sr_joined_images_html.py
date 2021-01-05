import argparse
import pandas as pd


parser = argparse.ArgumentParser(description='Process arguments.')
parser.add_argument('--input_file', type=str, default='/projects/ncdot/secondary_road/model_2lane_predict_d4_subset.csv',
                    help='input image file with model prediction')
parser.add_argument('--output_html_file', type=str, default='/projects/ncdot/secondary_road/model_2lane_d4_subset.html',
                    help='the output html file for looking at images')

args = parser.parse_args()
input_file = args.input_file
output_html_file = args.output_html_file

df = pd.read_csv(input_file, header=0, dtype=str, usecols=['file', 'prediction', 'class'])
print(df.shape)
df['file'] = df['file'].str.slice(start=len('images/'))
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
<div style="display: flex;">
    <img src='/get_image_by_name/{image_base_name}' style="float:left;width:100%;"/>    
</div>
<p>Image base name: {image_base_name}, prediction: {pred_class}({prob})</p>
"""
img_str_list = []
df.apply(lambda row: img_str_list.append(img_str.format(image_base_name=row['file'],
                                                        pred_class=row['class'],
                                                        prob=row['prediction'])), axis=1)
html_img_str = '\n'.join(img_str_list)
html_str = f"{html_str_head}\n{html_img_str}\n{html_str_tail}"
with open(output_html_file, 'w') as file:
    file.write(html_str)
