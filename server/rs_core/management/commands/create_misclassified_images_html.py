import pandas as pd

from django.core.management.base import BaseCommand

from rs_core.models import RouteImage


class Command(BaseCommand):
    """
    This script outputs html file for misclassified images for easy inspection
    To run this command, do:
    docker exec dot-server python manage.py create_misclassified_images_html <output_html_file_name_with_path>
    docker exec dot-server python manage.py create_misclassified_images_html
    <output_html_file_name_with_path> --model_predict_file <model_prediction_file> --labeled_file <labeled_file>
    --filter_2lanes
    For example:
    docker exec -ti dot-server python manage.py create_misclassified_images_html templates/show_misclassified_images.html
    """
    help = "Create misclassified images html file for easy inspection"

    def add_arguments(self, parser):
        # csv filename with full path to load metadata from
        parser.add_argument('output_html_file', help='output html file name with full path')
        parser.add_argument('--model_predict_file', type=str,
                            help=('Optional. The classifier model prediction output file'))
        parser.add_argument('--labeled_file', type=str,
                            help=('Optional. The labeled file to compare prediction with'))
        parser.add_argument('--filter_2lanes', action='store_true',
                            help=('Optional. If set to True, resulting image set only contains 2 lanes images'))

    def handle(self, *args, **options):
        output_html_file = options['output_html_file']
        input_pred_file = options['model_predict_file']
        if not input_pred_file:
            input_pred_file = 'metadata/guardrail_classification.csv'
        labeled_file = options['labeled_file']
        if not labeled_file:
            labeled_file = 'metadata/training_Image_guardrail_yn.csv'
        filter_2lanes = options['filter_2lanes']
        print('filter_2lanes: ', filter_2lanes)
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
        <p>Prediction probability: {probability}. Image base name: {image_base_name}</p>
        """
        pred_df = pd.read_csv(input_pred_file, header=0, index_col='MAPPED_IMAGE',
                              dtype={'MAPPED_IMAGE': 'str', 'Probability': 'float'})
        pred_df.dropna(inplace=True)
        print('prediction dataframe shape after removing NA:', pred_df.shape)
        label_df = pd.read_csv(labeled_file, header=0, index_col='MAPPED_IMAGE', dtype=str,
                               usecols=["MAPPED_IMAGE", "GUARDRAIL_YN"])
        print('labeled dataframe shape:', label_df.shape)
        concat_df = pd.concat([pred_df, label_df], axis=1, sort=False)
        print('concat_df shape:', concat_df.shape)
        misclassified_df_n = concat_df[(concat_df['Probability'] <= 0.1) & (concat_df['GUARDRAIL_YN'] == 'Y')]
        print(misclassified_df_n.shape)
        if filter_2lanes:
            image_list = list(RouteImage.objects.values_list("image_base_name", flat=True))
            misclassified_df_n = misclassified_df_n[misclassified_df_n.index.isin(image_list)]
            print("After filtering 2 lanes: ", misclassified_df_n.shape)
        img_str_list = []
        misclassified_df_n = misclassified_df_n.sample(n=100, random_state=1)
        print(misclassified_df_n.shape)
        misclassified_df_n.apply(lambda row: img_str_list.append(img_str.format(image_base_name=row.name,
                                                                            probability=row['Probability'])), axis=1)
        html_img_str = '\n'.join(img_str_list)
        html_str = f"{html_str_head}\n{html_img_str}\n{html_str_tail}"
        with open(output_html_file, 'w') as file:
            file.write(html_str)
