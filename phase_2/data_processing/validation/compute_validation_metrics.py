import pandas as pd
import numpy as np
import argparse
import sys
from common.utils import haversine
import matplotlib.pyplot as plt


def detection_metrics(pairs_df, all_pred_df, threshold):
    """
    Compute TP, FP, FN using:
      - pairs_df: dataframe of matched pairs with distance_col included
      - all_pred_df: dataframe of all predicted poles
      - threshold: distance threshold in meters
    """
    # --- TP and FP from matched pairs ---
    tp = np.sum(pairs_df[distance_col] <= threshold)
    fp = np.sum(pairs_df[distance_col] > threshold)

    # --- FN from full validated set ---
    # validated poles
    val_lats = pairs_df["LIDAR_LATITUDE"].values
    val_lons = pairs_df["LIDAR_LONGITUDE"].values

    # all predictions
    pred_lats = all_pred_df["LATITUDE"].values
    pred_lons = all_pred_df["LONGITUDE"].values

    # compute distance matrix (val x pred)
    dist_matrix = haversine(
        val_lons[:, None], val_lats[:, None],
        pred_lons[None, :], pred_lats[None, :]
    )
    # nearest prediction distance for each validated pole
    min_dists = dist_matrix.min(axis=1)
    # FN = validated poles with no predictions within threshold
    fn = np.sum(min_dists > threshold)
    # --- Metrics ---
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "Threshold (m)": threshold,
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "Precision": precision,
        "Recall": recall,
        "F1": f1,
    }

def sweep_thresholds_from_df(df, all_pred_df):
    """
    Compute metrics across multiple thresholds and return a DataFrame.
    """
    results = [detection_metrics(df, all_pred_df, t) for t in thresholds]
    return pd.DataFrame(results)

def plot_f1_vs_threshold(results_df, title, out_file):
    """
    Plot F1 score vs. threshold from validation results.
    """
    plt.figure(figsize=(6,4))
    plt.plot(results_df["Threshold (m)"], results_df["F1"], marker='o', linestyle='-')
    plt.xlabel("Threshold (m)")
    plt.ylabel("F1 score")
    plt.title(title)
    plt.ylim(0, 1)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.savefig(out_file, format=out_file.split('.')[-1], dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved figure to {out_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process input arguments.')
    parser.add_argument('--validation_pair_input_file', type=str,
                        default='../data/d13_route_40001001012/validation_mapping_output.csv',
                        help='input file name with path that contains validation results for 29 pole pairs')

    parser.add_argument('--all_geotag_input_file', type=str,
                        default='../data/d13_route_40001001012/route_40001001012_mapping_output_processed.csv',
                        help='input file name with path that contains all geotagged results for 180 poles')

    parser.add_argument('--distance_col', type=str,
                        default='Distance offset',
                        help='the column in the input_file that represents distance to compare with threshold')

    args = parser.parse_args()
    validation_pair_input_file = args.validation_pair_input_file
    all_geotag_input_file = args.all_geotag_input_file
    distance_col = args.distance_col

    thresholds = np.arange(2, 20, 1)

    pair_df = pd.read_csv(validation_pair_input_file, usecols=['LIDAR_LATITUDE', 'LIDAR_LONGITUDE', distance_col])
    all_df = pd.read_csv(all_geotag_input_file, usecols=['LATITUDE', 'LONGITUDE'])
    # Example: Geodesic distance metrics
    geo_results = sweep_thresholds_from_df(pair_df, all_df)
    print("\nGeodesic distance results:\n", geo_results)

    # Plot f1-vs-threshold curve
    plot_f1_vs_threshold(geo_results, "F1 Score vs. Geodesic Distance Threshold",
                         "geodesic_f1_vs_threshold.pdf")

    sys.exit(0)
