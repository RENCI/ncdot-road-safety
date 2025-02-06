import os
import glob
import argparse
import numpy as np
import polars as pl
from scipy import ndimage
import laspy
import skimage


class Rasterizer:
    def __init__(
            self,
            df=None,
            road_class=11,
            bridge_class=17,
            raster_type="normalized",
            hit_type="highest",
            edge_hit="highest",
            x_lims=None,
            y_lims=None,
    ):
        self.df = df
        self.road_class = road_class
        self.bridge_class = bridge_class
        self.raster_type = raster_type
        self.hit_type = hit_type
        self.edge_hit = edge_hit
        self.x_lims = x_lims
        self.y_lims = y_lims

    def get_lidar_data(self, las_files):
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
        self.create_df(point_data)

    def create_df(self, point_data):
        print("Creating dataframe...")
        df = pl.DataFrame(
            {
                "RAW_X": point_data[:, 0] / 100,
                "RAW_Y": point_data[:, 1] / 100,
                "RAW_Z": point_data[:, 2] / 100,
                "RAW_C": point_data[:, 3]
            }
        )

        if self.x_lims and self.y_lims:
            df = df.filter(
                (pl.col("RAW_X") >= min(self.x_lims)) &
                (pl.col("RAW_X") <= max(self.x_lims)) &
                (pl.col("RAW_Y") >= min(self.y_lims)) &
                (pl.col("RAW_Y") <= max(self.y_lims))
            )

        df = df.with_columns(
            pl.col("RAW_X").cast(pl.Int32).alias("VOX_X"),
            pl.col("RAW_Y").cast(pl.Int32).alias("VOX_Y"),
            pl.col("RAW_Z").cast(pl.Int16).alias("VOX_Z"),
            (pl.col("RAW_C") == 11).alias("ROAD"),
            (pl.col("RAW_C") == 17).alias("BRIDGE")
        )

        self.rasterize(df)

    def rasterize(self, df):
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
        self.df = q.collect()
        self.df = self.df.with_columns(
            pl.col("VOX_X").cast(pl.Int32).alias("VOX_X"),
            pl.col("VOX_Y").cast(pl.Int32).alias("VOX_Y"),
            pl.col("VOX_Z").cast(pl.Int16).alias("VOX_Z"),
            pl.col("C").list.tail(1).explode().alias("C")
        )

        print(f"Rasterized data points: {len(self.df)}")

    def get_hits(self):
        for hit in ["lowest", "highest"]:
            print(f"Getting {hit} hit voxels...")
            col_name = {
                "lowest": "LOWEST_HIT",
                "highest": "HIGHEST_HIT",
            }

            agg_func = {
                "lowest": pl.col("VOX_Z").min().alias("VOX_Z"),
                "highest": pl.col("VOX_Z").max().alias("VOX_Z"),
            }

            q = (
                self.df.lazy()
                .group_by("VOX_X", "VOX_Y")
                .agg(agg_func[hit])
                .sort("VOX_X", "VOX_Y")
            )

            hits = q.collect()
            hits = hits.with_columns(
                pl.Series(np.ones(len(hits), dtype=bool)).alias(col_name[hit]),
                pl.col("VOX_Z").cast(pl.Int16).alias("VOX_Z")
            )

            print(f"Found {len(hits)} {hit} hit voxels.\nMerging...")

            self.df = (
                self.df.join(
                    hits,
                    on=["VOX_X", "VOX_Y", "VOX_Z"],
                    how="left",
                    coalesce=True
                )
                .fill_null(False)
            )

            print("Done.")

    def fix_road_and_bridge(self):
        print("Fixing road and bridge...")
        self.df = self.df.with_columns(
            pl.when(pl.col("ANY_BRIDGE"))
            .then(self.bridge_class)
            .when(pl.col("ANY_ROAD"))
            .then(self.road_class)
            .otherwise(pl.col("C"))
            .alias("C")
        )

    def find_edges(self):
        """
        Make a 2D top down image of road/bridge and use edge detection to find voxels on edge of road
        :param df:
        :param road_class:
        :param bridge_class:
        :param hit: Use "highest" or "lowest" hits of road/bridge per x/y (not necessarily the highest/lowest hit for all
            points in that x/y)
        :return:
        """
        print("Finding edges...")

        # By looping through all rows, the z_image will store only the final z value encountered for a given x, y.
        # Therefor, sorting VOX_Z in descending order will result in the lowest hit, while ascending will give the highest.
        assert self.edge_hit in ["highest", "lowest"], "Invalid hit type requested. Must be either 'highest' or 'lowest'"
        if self.edge_hit == "highest":
            desc = False
        elif self.edge_hit == "lowest":
            desc = True

        q = (
            self.df.lazy()
            .filter((pl.col("C") == self.road_class) | (pl.col("C") == self.bridge_class))
            .select(["VOX_Y", "VOX_X", "VOX_Z"])
            .sort("VOX_Z", descending=desc)
        )

        road = q.collect().to_numpy()
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

        self.create_edge_df(xy_image, z_image, mins)

    def create_edge_df(self, edge_image, height_image, mins):
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

        self.join_edges(edge_df)

    def join_edges(self, edge_df):
        print("Joining dataframes...")
        self.df = self.df.join(edge_df, on=["VOX_X", "VOX_Y", "VOX_Z"], how="left").fill_null(False)
        self.df = self.df.with_columns(
            pl.col("EDGE").cast(pl.Int8).alias("EDGE"),
            pl.col("LOWEST_HIT").cast(pl.Int8).alias("LOWEST_HIT"),
            pl.col("HIGHEST_HIT").cast(pl.Int8).alias("HIGHEST_HIT")
        )

        print(f"Edge data points: {self.df['EDGE'].sum()}")

    def reduce_hit_types(self, output_columns):
        q = (
            self.df.lazy()
            .filter((pl.col("EDGE") == 1) | (pl.col(f"{self.hit_type.upper()}_HIT") == 1))
            .select(output_columns)
        )

        self.df = q.collect()

    def write_to_file(self, output_path):
        print("Writing output file...")
        self.df.write_csv(output_path)
        print("Done.")


    def run(
            self,
            input_path,
            extension
    ):
        if extension.startswith("."):
            extension = extension[1:]

        if os.path.isdir(input_path):
            las_files = glob.glob(os.path.join(input_path, f"*.{extension}"))
        else:
            assert (input_path.endswith(".las") or input_path.endswith(".laz")), "Invalid file type (.las or .laz)"
            las_files = [input_path]

        raster_columns = {
            "barycenter": ["X", "Y", "Z", "C", "EDGE"],
            "normalized": ["VOX_X", "VOX_Y", "VOX_Z", "C", "EDGE"]
        }

        self.get_lidar_data(las_files)
        self.fix_road_and_bridge()
        self.get_hits()
        self.find_edges()

        output_columns = raster_columns[self.raster_type]
        if self.hit_type == "all":
            output_columns.extend(["LOWEST_HIT", "HIGHEST_HIT"])
            self.df = self.df.select(output_columns)
        else:
            self.reduce_hit_types(output_columns)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--input_path',
        type=str,
        default="/projects/ncdot/secondary_road/new_lidar/Buffer50/30ppsm/",
        help='input path'
    )
    parser.add_argument(
        '-o',
        '--output_path',
        type=str,
        default="./route_40001001012_voxel_raster_1ft_with_edges.csv",
        help='output file'
    )
    parser.add_argument(
        '-e',
        '--extension',
        type=str,
        default='las',
        help='extension of input files'
    )
    parser.add_argument(
        '-r',
        '--road_class',
        type=int,
        default=11,
        help='road class value. new scene = 11, old scene = 13'
    )
    parser.add_argument(
        '-b',
        '--bridge_class',
        type=int,
        default=17,
        help='bridge class value. new scene = 17, old scene = 14'
    )
    parser.add_argument(
        '-t',
        '--raster_type',
        type=str,
        choices=['normalized', 'barycenter'],
        default='normalized',
        help='Raster type: "normalized" (point placed at grid coordinate of occupied voxels) or "barycenter" (point placed at mean coordinate of points within each voxel)')
    parser.add_argument(
        '-H',
        '--hit_type',
        type=str,
        choices=['highest', 'lowest', 'all'],
        default='highest',
        help='Limit to highest or lowest populated voxel in each grid coordinate, or return all points. All points output includes LOWEST_HIT and HIGHEST_HIT columns'
    )
    parser.add_argument(
        '--xmin',
        type=int,
        default=None,
        help='X min for bounding box'
    )
    parser.add_argument(
        '--xmax',
        type=int,
        default=None,
        help='X max for bounding box'
    )
    parser.add_argument(
        '--ymin',
        type=int,
        default=None,
        help='Y min for bounding box'
    )
    parser.add_argument(
        '--ymax',
        type=int,
        default=None,
        help='Y max for bounding box'
    )


    ARGS = parser.parse_args()
    input_path = ARGS.input_path
    output_path = ARGS.output_path
    extension = ARGS.extension
    road_class = ARGS.road_class
    bridge_class = ARGS.bridge_class
    raster_type = ARGS.raster_type
    hit_type = ARGS.hit_type
    xmin = ARGS.xmin
    xmax = ARGS.xmax
    ymin = ARGS.ymin
    ymax = ARGS.ymax

    rasterizer = Rasterizer(
        road_class=road_class,
        bridge_class=bridge_class,
        raster_type=raster_type,
        hit_type=hit_type,
        x_lims=(xmin, xmax),
        y_lims=(ymin, ymax)
    )
    rasterizer.run(input_path, extension)
    rasterizer.write_to_file(output_path)
