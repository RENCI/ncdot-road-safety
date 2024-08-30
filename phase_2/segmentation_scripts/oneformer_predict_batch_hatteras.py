#!/usr/bin/env python
import warnings
import multiprocessing as mp
import os
import random
import argparse
import glob
# fmt: off
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# fmt: on

import cv2
import numpy as np
import pandas as pd
import torch
import tqdm

from detectron2.config import get_cfg
from detectron2.checkpoint import DetectionCheckpointer
from detectron2.projects.deeplab import add_deeplab_config
from detectron2.utils.logger import setup_logger
from detectron2.modeling import build_model

from oneformer import (
    add_oneformer_config,
    add_common_config,
    add_swin_config,
    add_dinat_config,
    add_convnext_config,
)

from dot import DOTDataset, DOTPredictor


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model',
        required=True,
        type=str,
        choices=[
            "convnext_l",
            "convnext_xl",
            "dinat_l",
            "swin_l",
            "mapillary_convnext_l",
            "mapillary_convnext_xl",
        ],
        help='Model to use for segmentation')

    # One of these is required
    parser.add_argument('--csv_path', type=str, default=None, help='Path to CSV of image paths')
    parser.add_argument('--input_directory', type=str, default=None, help='Path to input directory')

    parser.add_argument('--weights_dir', type=str, default="OneFormer/models", help='Path to weights folder')
    parser.add_argument('--image_column', type=str, default='MAPPED_IMAGE', help='Image column header')
    parser.add_argument('--path_column', type=str, default='PATH', help='Path column header')
    parser.add_argument("--config_dir", type=str, default="OneFormer/configs", help="path to config folder")
    parser.add_argument("--output", required=True, help="A directory to save output visualizations. ")
    parser.add_argument("--confidence-threshold", type=float, default=0.5, help="Minimum score for instance predictions to be shown")
    parser.add_argument('--num_images', type=int, default=None, help='Number of images to annotate')
    parser.add_argument("--hong_paths", action='store_true', help='Paths from Hongs sheet')
    parser.add_argument("--height", type=int, default=None)
    parser.add_argument("--max_width", type=int, default=None)
    parser.add_argument("--batch", type=int, default=1, help="Images per batch")

    return parser


def setup_cfg(config_file, opts):
    # load config from file and command-line arguments
    cfg = get_cfg()
    add_deeplab_config(cfg)
    add_common_config(cfg)
    add_swin_config(cfg)
    add_dinat_config(cfg)
    add_convnext_config(cfg)
    add_oneformer_config(cfg)
    cfg.merge_from_file(config_file)
    cfg.merge_from_list(opts)
    cfg.freeze()

    return cfg


def main():
    warnings.filterwarnings("ignore", category=UserWarning)
    args = get_parser().parse_args()

    assert args.csv_path or args.input_directory, "No input method given, expected either a CSV or input directory."
    assert not (args.csv_path and args.input_directory), "Expected either a CSV or input directory, detected both."

    print("cuda gpu device count:", torch.cuda.device_count())
    gpu = torch.cuda.current_device()
    print("cuda currently selected gpu device: ", gpu)

    if args.input_directory:
        imgs = glob.glob(os.path.join(args.input_directory, "**/*.jpg"), recursive=True)
        imgs = [img for img in imgs if not img.split("/")[-1].replace(".jpg", "").endswith("6")]

    if args.csv_path:
        # Get DOT images
        # Columns: MAPPED_IMAGE, PATH
        image_csv = pd.read_csv(args.csv_path, dtype='str')
        imgs = []
        for i, image in enumerate(image_csv[args.image_column]):
            if args.hong_paths:
                image_path = image_csv.loc[i, args.image_column].replace('.jpg','')
                if 'd4' in image_path:
                    image_path = image_path.replace('d4', 'd04')
                elif 'd8' in image_path:
                    image_path = image_path.replace('d8', 'd08')
                base_path = os.path.join('/projects/ncdot/NC_2018_Secondary', image_path)
            else:
                base_path = os.path.join(image_csv.loc[i, args.path_column], image_csv.loc[i, args.image_column])

            views = [base_path + '{0}.jpg'.format(view) for view in [5,1,2]] # left, center, right
            imgs.extend(views)

    if args.num_images is not None:
        imgs = imgs[:args.num_images]

    # Set up model
    seed = 0
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    model_dict = {
        "convnext_l": {
            "weights_file": os.path.join(args.weights_dir, "250_16_convnext_l_oneformer_cityscapes_90k.pth"),
            "config_file": os.path.join(args.config_dir, "cityscapes/convnext/oneformer_convnext_large_bs16_90k.yaml")
        },
        "convnext_xl": {
            "weights_file": os.path.join(args.weights_dir, "250_16_convnext_xl_oneformer_cityscapes_90k.pth"),
            "config_file": os.path.join(args.config_dir, "cityscapes/convnext/oneformer_convnext_xlarge_bs16_90k.yaml")
        },
        "dinat_l": {
            "weights_file": os.path.join(args.weights_dir, "250_16_dinat_l_oneformer_cityscapes_90k.pth"),
            "config_file": os.path.join(args.config_dir, "cityscapes/dinat/oneformer_dinat_large_bs16_90k.yaml")
        },
        "swin_l": {
            "weights_file": os.path.join(args.weights_dir, "250_16_swin_l_oneformer_cityscapes_90k.pth"),
            "config_file": os.path.join(args.config_dir, "cityscapes/swin/oneformer_swin_large_bs16_90k.yaml")
        },
        "mapillary_convnext_l": {
            "weights_file": os.path.join(args.weights_dir, "mapillary_pretrain_250_16_convnext_l_oneformer_cityscapes_90k.pth"),
            "config_file": os.path.join(args.config_dir, "cityscapes/convnext/mapillary_pretrain_oneformer_convnext_large_bs16_90k.yaml")
        },
        "mapillary_convnext_xl": {
            "weights_file": os.path.join(args.weights_dir, "mapillary_pretrain_250_16_convnext_xl_oneformer_cityscapes_90k.pth"),
            "config_file": os.path.join(args.config_dir, "cityscapes/convnext/mapillary_pretrain_oneformer_convnext_xlarge_bs16_90k.yaml")
        }
    }

    config_path = model_dict[args.model]["config_file"]
    weights_path = model_dict[args.model]["weights_file"]
    opts = ["MODEL.IS_TRAIN", "False", "MODEL.WEIGHTS", weights_path]

    mp.set_start_method("spawn", force=True)
    setup_logger(name="fvcore")
    logger = setup_logger()
    logger.info("Arguments: " + str(config_path) + str(opts))

    cfg = setup_cfg(config_file=config_path, opts=opts)
    model = build_model(cfg)
    model.eval()
    checkpointer = DetectionCheckpointer(model)
    checkpointer.load(cfg.MODEL.WEIGHTS)

    # Register dataset
    dataset = DOTDataset(imgs).map_dicts()
    predictor = DOTPredictor(height=args.height, max_width=args.max_width, batch_size=args.batch)

    os.makedirs(args.output, exist_ok=True)
    
    with tqdm.tqdm(total=len(dataset)) as pbar:
        while predictor.current_index < len(dataset):
            predictions = predictor(dataset, model)
            for pred in predictions:
                pred_label = pred[0].cpu().argmax(dim=0).numpy().astype(np.uint8)
                out_filename = pred[1].replace(".jpg", ".png")
                cv2.imwrite(out_filename, pred_label)

            pbar.update(args.batch)

    print("Inference complete.")


if __name__ == '__main__':
    main()
