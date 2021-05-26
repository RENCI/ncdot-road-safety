from django.core.management.base import BaseCommand
from django.conf import settings
import pandas as pd
import random
from rs_core.models import RouteImage
from rs_core.utils import save_user_annot_summary_to_db, save_holdout_test_info_to_db


class Command(BaseCommand):
    """
    This script loads holdout test info for a specified active learning round into database
    To run this command, do:
    docker exec -ti dot-server python manage.py load_holdout_test_info <input_prediction_csv_file_with_path>
    <input_annot_csv_file_with_path> <annotation_name> <round_number>
    For example:
    docker exec -ti dot-server python manage.py load_holdout_test_info
    /projects/ncdot/NC_2018_Secondary/active_learning/guardrail/round5/predict/model_predict_test.csv
    /projects/ncdot/NC_2018_Secondary/active_learning/guardrail/holdout_test/annot_data/user_annoted_image_info.csv
    guardrail 5
    """
    help = "Process the user annotation file in csv format to compute summary and load into database"

    def add_arguments(self, parser):
        parser.add_argument('input_predict_file', help='input model prediction csv file name with full path to be '
                                                       'processed and load user holdout test info from')
        parser.add_argument('input_annot_file', help='input user annotation csv file name with full path to be '
                                                     'processed and load user holdout test info from')
        parser.add_argument('annot_name', help='annotation name for which holdout test info needs to be saved')
        parser.add_argument('round_number', help='The AL round number for the holdout test info to be loaded')


    def handle(self, *args, **options):
        input_predict_file = options['input_predict_file']
        input_annot_file = options['input_annot_file']
        annot_name = options['annot_name']
        round_no = options['round_number']
        if settings.USE_IRODS:
            # randomly create some data for local development
            index = 0
            for obj in RouteImage.objects.all():
                presence = True if index % 2 == 0 else False
                certainty = round(random.uniform(0.5, 1), 2) if index % 3 == 0 else round(random.uniform(0, 0.5), 2)
                save_holdout_test_info_to_db(obj.image_base_name, annot_name, round_no,
                                             presence,
                                             True,
                                             certainty,
                                             0, certainty, 0)
                index += 1
        else:
            pred_df = pd.read_csv(input_predict_file, header=0, index_col='MAPPED_IMAGE',
                                  dtype={'MAPPED_IMAGE': str, 'ROUND_PREDICT': float})
            annot_df = pd.read_csv(input_annot_file, header=0, index_col='Image', dtype={'Image': str,
                                                                                         'Presence': bool,
                                                                                         'IN_BALANCE_SET': bool})
            pred_df.index = pred_df.index.str.split('/').str[-1]
            pred_df.index = pred_df.index.str.replace('.jpg', '')
            if len(pred_df.index[0]) == 12:
                pred_df['LeftView'] = pred_df.apply(lambda row: row.ROUND_PREDICT if row.name.endswith('5') else 0,
                                                    axis=1)
                pred_df['FrontView'] = pred_df.apply(lambda row: row.ROUND_PREDICT if row.name.endswith('1') else 0,
                                                     axis=1)
                pred_df['RightView'] = pred_df.apply(lambda row: row.ROUND_PREDICT if row.name.endswith('2') else 0,
                                                     axis=1)
                pred_df['GROUP'] = pred_df.index.str[:-1]
                pred_df['ROUND_PREDICT_GROUP'] = pred_df.apply(lambda row: 1 if row.ROUND_PREDICT >= 0.5 else 0,
                                                               axis=1)
                pred_df.drop(columns=['ROUND_PREDICT'], inplace=True)
                pred_df.rename(columns={'ROUND_PREDICT_GROUP': 'ROUND_PREDICT'}, inplace=True)
                pred_df = pred_df.groupby(by=['GROUP']).sum()
            else:
                pred_df['LeftView'] = pred_df['ROUND_PREDICT']
                pred_df['FrontView'] = pred_df['ROUND_PREDICT']
                pred_df['RightView'] = pred_df['ROUND_PREDICT']

            annot_df.index = annot_df.index.str.split('/').str[-1]
            annot_df.index = annot_df.index.str.replace('.jpg', '')
            concat_df = pd.concat([pred_df, annot_df], axis=1)
            print(pred_df.shape, annot_df.shape, concat_df.shape)
            concat_df.apply(lambda row: save_holdout_test_info_to_db(row.name, annot_name, round_no,
                                                                     row.Presence, row.IN_BALANCE_SET,
                                                                     row.ROUND_PREDICT,
                                                                     row.LeftView, row.FrontView, row.RightView), axis=1)
        print('Done')
