import itertools
import multiprocessing as mp
import numpy as np
import pandas as pd
from scipy.spatial import Delaunay
from typing import List
from utils import LIDARClass


class QuadTree:
    """
    Data structure for fast lookup of projected lidar points in 2D screen space
    """
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # Rectangle boundary (x, y, width, height)
        self.capacity = capacity  # Max points per quadrant
        self.points = []
        self.indices = []  # Indices to reference triangle array
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None
        self.divided = False

    def subdivide(self):
        """ Split current boundary into four subdivisions """
        x, y, w, h = self.boundary
        hw, hh = w / 2, h / 2

        self.nw = QuadTree((x, y, hw, hh), self.capacity)
        self.ne = QuadTree((x + hw, y, hw, hh), self.capacity)
        self.sw = QuadTree((x, y + hh, hw, hh), self.capacity)
        self.se = QuadTree((x + hw, y + hh, hw, hh), self.capacity)
        self.divided = True

    def insert(self, point, index):
        """ Insert new point into tree """
        if not self.contains(self.boundary, point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            self.indices.append(index)
            return True

        if not self.divided:
            self.subdivide()

        if self.nw.insert(point, index):
            return True
        if self.ne.insert(point, index):
            return True
        if self.sw.insert(point, index):
            return True
        if self.se.insert(point, index):
            return True

    def query(self, rects):
        """ Return points within a target bounding box"""
        if isinstance(rects, tuple):
            rects = [rects]

        rects = np.array(rects)

        found = []
        for i, rect in enumerate(rects):
            if not self.intersects(self.boundary, rect):
                continue

            for idx, p in zip(self.indices, self.points):
                if self.contains(rect, p):
                    found.append((idx, p))

            if self.divided:
                found.extend(self.nw.query(rects))
                found.extend(self.ne.query(rects))
                found.extend(self.sw.query(rects))
                found.extend(self.se.query(rects))

        return found

    @staticmethod
    def contains(rect, point):
        """ Check if a point is within a target bounding box """
        x, y, w, h = rect
        px, py = point

        return (x <= px < x + w) and (y <= py < y + h)

    @staticmethod
    def intersects(rect1, rect2):
        """ Check if two bounding boxes overlap """
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2

        return not (x2 > x1 + w1 or x2 + w2 < x1 or y2 > y1 + h1 or y2 + h2 < y1)

    @staticmethod
    def rect_from_point(point, rect_h, rect_w, max_x, max_y):
        """ Create a bounding box centered on a point """
        x, y = point

        # Define the target bounding box
        rect_x_min = max(x - rect_w / 2, 0)
        rect_y_min = max(y - rect_h / 2, 0)
        rect_x_max = min(x + rect_w / 2, max_x)
        rect_y_max = min(y + rect_h / 2, max_y)

        rect_w = rect_x_max - rect_x_min
        rect_h = rect_y_max - rect_y_min

        return (rect_x_min, rect_y_min, rect_w, rect_h)


def calculate_surface_normals(triangles: np.ndarray) -> np.ndarray:
    """
    Calculate surface normals of triangles
    :param triangles: Numpy array of triangles
    :return: Numpy array of surface normals
    """
    AB = triangles[:, 1] - triangles[:, 0]
    AC = triangles[:, 2] - triangles[:, 0]
    normals = np.cross(AB, AC)

    # Normalize the normals
    normals /= np.linalg.norm(normals, axis=1)[:, np.newaxis]

    return normals


def ray_triangle_intersection(
        ray_origin: np.ndarray,
        ray_target: np.ndarray,
        triangle_vertices: np.ndarray,
        epsilon: float = 1e-6
) -> bool:
    """
    Möller–Trumbore triangle intersection algorithm
    :param ray_origin: Coordinates of ray origin
    :param ray_target: Coordinates of ray target
    :param triangle_vertices: (N, 3, 3) Numpy array containing coordinates of triangle vertices
    :param epsilon: Threshold beneath which rays are parallel to triangle face and therefore do not intersect
    :return: True if ray intersection exists, False otherwise
    """
    ray = ray_target - ray_origin
    ray_mag = np.linalg.norm(ray)
    ray_direction = ray / ray_mag

    edge1 = triangle_vertices[:, 1] - triangle_vertices[:, 0]
    edge2 = triangle_vertices[:, 2] - triangle_vertices[:, 0]
    normals = np.cross(edge1, edge2)

    # get triangles with dot products less than 0 meaning they are facing the ray rather than facing away from the ray
    facing_ray = np.sum(normals * ray_direction, axis=1) < 0

    h = np.cross(ray_direction, edge2)

    det = np.sum(edge1 * h, axis=1)
    # when det is close to 0, the ray is nearly parallel to the triangle plane. Assigning np.inf prevents
    # divisions by zero and also makes inv_det = 0, thus treating parallel rays as non-intersections.
    det[np.abs(det) < epsilon] = np.inf

    inv_det = 1.0 / det
    s = ray_origin - triangle_vertices[:, 0]
    u = inv_det * np.sum(s * h, axis=1)
    q = np.cross(s, edge1)
    v = inv_det * np.sum(ray_direction * q, axis=1)
    t = inv_det * np.sum(edge2 * q, axis=1)

    intersected = np.logical_and.reduce(
        [facing_ray, u >= 0.0, v >= 0.0, u + v <= 1.0, t > epsilon, t <= ray_mag]
    )

    return np.any(intersected)


def get_block_axis(block_dim: int, min_val: int, max_val: int) -> List[tuple]:
    """
    Get bounds for one axis of a series of blocks
    :param block_dim: Size of block dimension
    :param min_val: Starting location of first block
    :param max_val: Ending location of last block
    :return: List of tuples of (starting location, block dimension)
        Each block should have the same dimension, except the final block
        which will extend to the max value
    """
    block_start = min_val
    block_lims = []
    while True:
        block_end = block_start + block_dim
        if block_end >= max_val:
            block_lims.append((block_start, max_val - block_start))
            break

        block_lims.append((block_start, block_dim))
        block_start = block_end

    return block_lims


def create_blocks(image_width: int, image_height: int, block_count: int = 64) -> List[tuple]:
    """
    Create an array of rectangular bounds for block processing
    :param image_width: image width in pixels
    :param image_height: image height in pixels
    :param block_count: number of blocks per axis
    :return: list of tuples containing block rectangles (x, y, w, h)
    """
    block_dims = (int(np.ceil(image_width / block_count)), int(np.ceil(image_height / block_count)))
    block_x = get_block_axis(block_dims[0], 0, image_width)
    block_y = get_block_axis(block_dims[1], 0, image_height)

    return [(bx[0], by[0], bx[1], by[1]) for bx, by in itertools.product(block_x, block_y)]


def process_block(block_rect: tuple, epsilon: float = 1e-6) -> List[tuple]:
    """
    Perform raycasting for a rectangular section of an image. Find all projected points within the region,
    and cast a ray from the camera to each point, checking for intersections with any neighboring triangles.
    :param block_rect: Region bounds (x, y, w, h)
    :return: List of tuples with (point index, intersection Boolean)
        True = occluded
        False = visible
    """
    # Get global variables
    global vertices
    global simplices
    global camera_location
    global quad_tree

    # Query the point tree to find index of points in the block
    results = quad_tree.query(block_rect)
    if not results:
        return []

    found_indices, _ = zip(*results)

    # Find all triangles containing those points (including triangles extending outside the block)
    found_triangle_mask = np.any(np.isin(simplices, found_indices), axis=1)
    found_simplices = simplices[found_triangle_mask]

    # Cast a ray to each point and determine the visibility
    obstructed = []
    for index in found_indices:
        # Remove triangles containing the target point
        self_mask = ~np.any(np.isin(found_simplices, index), axis=1)
        found_triangles = vertices[found_simplices[self_mask]]
        if not len(found_triangles):
            obstructed.append((index, False))
            continue

        # Cast the ray
        obstructed.append(
            (index, ray_triangle_intersection(camera_location, vertices[index], found_triangles, epsilon))
        )

    return obstructed


def find_occluded_points(
        df: pd.DataFrame,
        camera_position: np.ndarray,
        image_width: int,
        image_height: int,
        ground_only: bool = True,
        lowest_hit: bool = True,
        block_count: int = 64
) -> pd.DataFrame:
    """
    Determine the visibility of all points in a dataframe. Global variables are set here so child processes can share
    the data. Points can optionally be filtered to include only ground and/or lowest hits. A column will be added to
    the dataframe reflecting the occlusion state of each lidar point.
    :param df: Dataframe of lidar points with x/y/z coord, projected screen coords, and labels (at minimum)
    :param camera_position: Numpy array of camera x/y/z coordinates (in lidar space)
    :param image_width: Image width in pixels
    :param image_height: Image height in pixels
    :param ground_only: Filter the points to only include ground (ground, lowest veg, road, bridge)
    :param lowest_hit: Only include points labeled as lowest hit for each x/y raster unit
    :param block_count: Number of blocks to divide each axis of image for neighbor queries. Fewer bocks capture more
        lidar points per block, leading to more triangles to test for occlusion for each ray. Fewer blocks return more
        accurate results but are much slower.
    :return: The input dataframe with a new Boolean column indicating whether the point was occluded or not.
        True = occluded
        False = visible
        Any points filtered out (e.g. not ground) will return False
    """
    # Declare global variables
    global vertices
    global simplices
    global camera_location
    global quad_tree

    # Cam location in lidar coordinates
    camera_location = camera_position

    #  Create filters
    lidar_filter = np.ones(len(df), dtype=bool)
    if ground_only:
        lidar_filter = np.logical_and(lidar_filter,
                                      np.array([c == LIDARClass.GROUND.value or c == LIDARClass.LOW_VEG.value
                                                or c == LIDARClass.ROAD.value or c == LIDARClass.POLE.value
                                                or c == LIDARClass.BUILDING.value
                                                for c in df["C"].astype(int)]))

    if lowest_hit:
        lidar_filter = np.logical_and(lidar_filter, df["LOWEST_HIT"].to_numpy())

    vertices = df[lidar_filter][["X", "Y", "Z"]].values
    proj_vertices = df[lidar_filter][["PROJ_SCREEN_X", "PROJ_SCREEN_Y"]].values
    proj_vertices[:, 1] = image_height - proj_vertices[:, 1]
    df_indices = df.reset_index()[lidar_filter].index

    # Triangulate mesh in 2D
    tri = Delaunay(vertices[:, :-1])

    # Mask out any edge triangles, which only have two neighbors (True if not edge)
    edge_mask = ~np.any(np.isin(tri.neighbors, -1), axis=1)
    simplices = tri.simplices[edge_mask]

    # Create the QuadTree
    boundary = (0, 0, image_width, image_height)
    quad_tree = QuadTree(boundary=boundary, capacity=8)

    # Index here is index in Numpy array, not the original df.
    # Original index can be mapped back with `df_indices`
    for index, point in enumerate(proj_vertices):
        quad_tree.insert(point, index)

    # Block creation
    block_rects = create_blocks(image_width, image_height, block_count)

    # Process blocks in parallel
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.map(process_block, block_rects)

    # Merge and sort the results. Array of tuples (Numpy index, Bool: True if obstructed)
    flat_results = []
    for result in results:
        flat_results.extend(result)

    flat_results = sorted(flat_results)

    # Construct occlusion column for df
    obstructed_mask = np.zeros(len(df), dtype=bool)
    for index, obstructed in flat_results:
        obstructed_mask[df_indices[index]] = obstructed

    df["OCCLUDED"] = obstructed_mask

    return df
