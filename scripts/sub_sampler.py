import numpy as np
import geopandas as gpd
from gpd_helper import GPDHelper


class SubSampler:
  """ Point Clouds Sampler Class that implements decimation and voxel grid sampling for reducing point cloud data density.
  """

  def __init__(self, input_epsg: int, output_epsg: int, df: gpd.GeoDataFrame):
    """
    Args:
        input_epsg (int): Coordinate reference system for use in transformations.
        output_epsg (int): A coordinate reference system that the user uses.
        df (gpd.GeoDataFrame): Geopandas data frame
    """
    self._gpd_helper = GPDHelper(input_epsg, output_epsg)
    self.df = self._gpd_helper.covert_crs(df)

  def get_points(self):
    """ Generates a NumPy array from point clouds data.
    """
    x = self.df.geometry.x
    y = self.df.geometry.y
    z = self.df.elevation
    return np.array([x, y, z]).transpose()

  def decimation(self, factor: int = 20) -> gpd.GeoDataFrame:
    """ Performs Simple Subsampling type, selects samples with a constant jump scale(factor).
        If we define a point cloud as a matrix (m x n), then the decimated cloud is obtained by keeping one row out of n of this matrix

    Args:
        factor (int, optional): Jump scale. Defaults to 20.

    Returns:
        gpd.GeoDataFrame: Interpolated geopandas data frame
    """
    points = self.get_points()
    decimated_points = points[::factor]
    return self._gpd_helper.get_dep_points(decimated_points)

  def get_voxel_grid(self, points: np.ndarray, voxel_size: float) -> tuple:
    """ Create a grid structure over the points, and For each small voxel, we test if it contains one or more points.

    Args:
        points (np.ndarray): A NumPy array; containing point cloud data.
        voxel_size (float): Area of a typical cubic cell in the grid (in square meters) that represents a point.

    Returns:
        tuple: [description]
    """

    nb_vox = np.ceil((np.max(points, axis=0)
                     - np.min(points, axis=0)) / voxel_size)
    non_empty_voxel_keys, inverse, nb_pts_per_voxel = np.unique(
        ((points - np.min(points, axis=0)) // voxel_size).astype(int), axis=0, return_inverse=True, return_counts=True)
    idx_pts_vox_sorted = np.argsort(inverse)
    return nb_vox, non_empty_voxel_keys, nb_pts_per_voxel, idx_pts_vox_sorted

  def grid_barycenter(self, voxel_size: int) -> gpd.GeoDataFrame:
    """ Performs Grid grid subsampling strategy that divides 3D space into regular cubic cells that are called voxels.
        For each cell of this grid, It only keeps a representative point, which is the barycenter of the points in that cell.
        This point is representative of the cell.

    Args:
        voxel_size (int): Area of a typical cubic cell in the grid (in square meters) that represents a point.

    Returns:
        gpd.GeoDataFrame: interpolated geopandas dataframe
    """
    last_seen = 0
    voxel_grid = {}
    grid_barycenter = []
    points = self.get_points()
    nb_vox, non_empty_voxel_keys, nb_pts_per_voxel, idx_pts_vox_sorted = self.get_voxel_grid(
      points, voxel_size)

    for idx, vox in enumerate(non_empty_voxel_keys):
      voxel_grid[tuple(
        vox)] = points[idx_pts_vox_sorted[last_seen:last_seen + nb_pts_per_voxel[idx]]]
      grid_barycenter.append(np.mean(voxel_grid[tuple(vox)], axis=0))
      last_seen += nb_pts_per_voxel[idx]
    sample_points = np.array(list(map(list, grid_barycenter)))
    return self._gpd_helper.get_dep_points(sample_points)

  def grid_candidate_center(self, voxel_size: int) -> gpd.GeoDataFrame:
    """ Performs Grid grid subsampling strategy that divides 3D space into regular cubic cells that are called voxels.
        For each cell of this grid, It only keeps a representative point, which is the closest point to the barycenter in that cell.
        This point is representative of the cell.

    Args:
        voxel_size (int): Area of a typical cubic cell in the grid (in square meters) that represents a point.

    Returns:
        gpd.GeoDataFrame: Interpolated geopandas data frame
    """
    last_seen = 0
    voxel_grid = {}
    grid_candidate_center = []
    points = self.get_points()
    nb_vox, non_empty_voxel_keys, nb_pts_per_voxel, idx_pts_vox_sorted = self.get_voxel_grid(
      points, voxel_size)

    for idx, vox in enumerate(non_empty_voxel_keys):
      voxel_grid[tuple(
        vox)] = points[idx_pts_vox_sorted[last_seen:last_seen + nb_pts_per_voxel[idx]]]
      grid_candidate_center.append(voxel_grid[tuple(vox)][np.linalg.norm(
        voxel_grid[tuple(vox)] - np.mean(voxel_grid[tuple(vox)], axis=0), axis=1).argmin()])
      last_seen += nb_pts_per_voxel[idx]

    sample_points = np.array(list(map(list, grid_candidate_center)))
    return self._gpd_helper.get_dep_points(sample_points)
