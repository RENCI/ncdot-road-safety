import os
import glob
import argparse
import numpy as np
import polars as pl
from scipy import ndimage
import laspy
import skimage


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_dir', type=str, default="/projects/ncdot/secondary_road/new_lidar/Buffer50/30ppsm/", help='input dir')
    parser.add_argument('-o', '--output_path', type=str, default="./route_40001001012_voxel_raster_1ft_with_edges.csv", help='output file')
    parser.add_argument('-e', '--extension', type=str, default='las', help='extension of input files')
    parser.add_argument('-r', '--road_class', type=int, default=11, help='road class value. new scene = 11, old scene = 13')
    parser.add_argument('-b', '--bridge_class', type=int, default=17, help='bridge class value. new scene = 17, old scene = 14')

    return parser

def get_lidar_data(las_files):
    print("Fetching data from files...")
    for i, las_file in enumerate(las_files):
        # Read the laz file
        las = laspy.read(las_file)

        # Extract all data points to numpy array (row: [x, y, z, class])
        points = np.stack([las.X, las.Y, las.Z, las.classification], axis=0).transpose((1, 0))

        # Add points to numpy array
        if i == 0:
            point_data = points
        else:
            point_data = np.concatenate((point_data, points))

    print(f"Lidar data points: {len(point_data)}")
    return create_df(point_data)

def create_df(point_data):
    print("Creating dataframe...")
    df = pl.DataFrame(
        {
            "RAW_X": point_data[:, 0] / 100,
            "RAW_Y": point_data[:, 1] / 100,
            "RAW_Z": point_data[:, 2] / 100,
            "RAW_C": point_data[:, 3]
        }
    )

    df = df.with_columns(
        pl.col("RAW_X").cast(pl.Int32).alias("VOX_X"),
        pl.col("RAW_Y").cast(pl.Int32).alias("VOX_Y"),
        pl.col("RAW_Z").cast(pl.Int16).alias("VOX_Z"),
        (pl.col("RAW_C") == 11).alias("ROAD"),
        (pl.col("RAW_C") == 17).alias("BRIDGE")
    )

    return df

def rasterize(df):
    print("Rasterizing...")
    q = (
        df.lazy()
        .group_by("VOX_X", "VOX_Y", "VOX_Z")
        .agg(
            pl.col("RAW_X").mean().alias("X"),
            pl.col("RAW_Y").mean().alias("Y"),
            pl.col("RAW_Z").mean().alias("Z"),
            pl.col("RAW_C").mode().alias("C"),
            pl.col("ROAD").any().alias("ANY_ROAD"),
            pl.col("BRIDGE").any().alias("ANY_BRIDGE")
        )
        .sort("VOX_X", "VOX_Y", "VOX_Z")
    )
    vox = q.collect()
    vox = vox.with_columns(
        pl.col("VOX_X").cast(pl.Int32).alias("VOX_X"),
        pl.col("VOX_Y").cast(pl.Int32).alias("VOX_Y"),
        pl.col("VOX_Z").cast(pl.Int16).alias("VOX_Z"),
        pl.col("C").list.tail(1).explode().alias("C")
    )

    print(f"Rasterized data points: {len(vox)}.")
    return vox

def get_lowest_highest_hits(df, hit_type):
    # Hit types: "low" or "high"
    print(f"Getting {hit_type}est hit voxels...")
    col_name = {
        "low": "LOWEST_HIT",
        "high": "HIGHEST_HIT",
    }

    agg_func = {
        "low": pl.col("VOX_Z").min().alias("VOX_Z"),
        "high": pl.col("VOX_Z").max().alias("VOX_Z"),
    }

    q = (
        df.lazy()
        .group_by("VOX_X", "VOX_Y")
        .agg(agg_func[hit_type])
        .sort("VOX_X", "VOX_Y")
    )

    hits = q.collect()
    hits = hits.with_columns(
        pl.Series(np.ones(len(hits), dtype=bool)).alias(col_name[hit_type]),
        pl.col("VOX_Z").cast(pl.Int16).alias("VOX_Z")
    )

    print(f"Found {len(hits)} {hit_type}est hit voxels.\nMerging...")

    df = (
        df.join(
            hits,
            on=["VOX_X", "VOX_Y", "VOX_Z"],
            how="left",
            coalesce=True
        )
        .fill_null(False)
    )

    print("Done.")
    return df

def fix_road_and_bridge(df, road_class, bridge_class):
    print("Fixing road and bridge...")
    df = df.with_columns(
        pl.when(pl.col("ANY_BRIDGE"))
        .then(bridge_class)
        .when(pl.col("ANY_ROAD"))
        .then(road_class)
        .otherwise(pl.col("C"))
        .alias("C")
    )

    return df

def find_edges(df, road_class, bridge_class):
    print("Finding edges...")
    road = (
        df.filter(
            ( ((pl.col("C") == road_class) | (pl.col("C") == bridge_class)) & (pl.col("LOWEST_HIT")) )
        )
        .select(["VOX_Y", "VOX_X", "VOX_Z"])
        .to_numpy()
    )

    mins = np.min(road[:, :-1], axis=0)
    road[:, :-1] -= mins.astype(int)
    maxes = np.max(road[:, :-1], axis=0)

    xy_image = np.zeros((maxes + 1), dtype=bool)
    z_image = np.zeros_like(xy_image, dtype=np.int16)
    for y, x, z in road:
        xy_image[(y, x)] = 1
        z_image[(y, x)] = z

    xy_image = ndimage.binary_fill_holes(xy_image)
    xy_image = skimage.segmentation.find_boundaries(xy_image, mode="inner")

    return create_edge_df(xy_image, z_image, mins)

def create_edge_df(edge_image, height_image, mins):
    print("Creating edge dataframe...")
    edge_df = pl.DataFrame(
        {
            "VOX_X": np.where(edge_image)[1] + mins[1],
            "VOX_Y": np.where(edge_image)[0] + mins[0],
            "VOX_Z": [height_image[tuple(coord)] for coord in np.argwhere(edge_image * height_image)],
            "EDGE": np.ones_like(np.where(edge_image)[0], dtype=bool)
        }
    )
    edge_df = edge_df.with_columns(
        pl.col("VOX_X").cast(pl.Int32).alias("VOX_X"),
        pl.col("VOX_Y").cast(pl.Int32).alias("VOX_Y"),
        pl.col("VOX_Z").cast(pl.Int16).alias("VOX_Z")
    )

    return edge_df

def join_dfs(df, edge_df, output_path):
    print("Joining dataframes...")
    df = df.join(edge_df, on=["VOX_X", "VOX_Y", "VOX_Z"], how="left").fill_null(False)

    # df = df.with_columns(
    #     pl.when(pl.col("EDGE").is_null())
    #     .then(pl.lit(False))
    #     .otherwise(pl.lit(True))
    #     .alias("EDGE")
    # )

    print(f"Edge data points: {df['EDGE'].sum()}")
    return df

def write_to_file(df, output_path):
    print("Writing output files...")
    df.select(pl.col(["X", "Y", "Z", "C", "EDGE", "LOWEST_HIT", "HIGHEST_HIT"])).write_csv(output_path)
    df.select(pl.col(["VOX_X", "VOX_Y", "VOX_Z", "C", "EDGE", "LOWEST_HIT", "HIGHEST_HIT"])).write_csv(output_path.replace(".csv", "_normalized.csv"))

    print("Done.")


if __name__ == "__main__":
    ARGS = get_parser().parse_args()
    input_dir = ARGS.input_dir
    output_path = ARGS.output_path
    extension = ARGS.extension
    road_class = ARGS.road_class
    bridge_class = ARGS.bridge_class

    if extension.startswith("."):
        extension = extension[1:]

    las_files = glob.glob(os.path.join(input_dir, f"*.{extension}"))
    vox_df = get_lidar_data(las_files)
    vox_df = rasterize(vox_df)
    vox_df = fix_road_and_bridge(vox_df, road_class=road_class, bridge_class=bridge_class)
    vox_df = get_lowest_highest_hits(vox_df, hit_type="low")
    vox_df = get_lowest_highest_hits(vox_df, hit_type="high")
    edge_df = find_edges(vox_df, road_class=road_class, bridge_class=bridge_class)
    vox_df = join_dfs(vox_df, edge_df, output_path)
    vox_df = vox_df.with_columns(
        pl.col("EDGE").cast(pl.Int8).alias("EDGE"),
        pl.col("LOWEST_HIT").cast(pl.Int8).alias("LOWEST_HIT"),
        pl.col("HIGHEST_HIT").cast(pl.Int8).alias("HIGHEST_HIT")
    )
    write_to_file(vox_df, output_path)
