import os
import elevation
import matplotlib
import numpy as np
import richdem as rd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import point
from gpd_helper import GPDHelper


class SubSampler:
  """ Point Clouds Sampler Class that can implement Factor, BaryCenter or Relative Distance Samplings .
  """

  def __init__(self, input_epsg: int, output_epsg: int, df: gpd.GeoDataFrame):
    self._gpd_helper = GPDHelper(input_epsg, output_epsg)
    self.df = self._gpd_helper.covert_crs(df)

  def get_points(self):
    """ Generate numpy array of points from point clouds data.
    """
    x = self.df.geometry.x
    y = self.df.geometry.y
    z = self.df.elevation
    return np.array([x, y, z]).transpose()

  def decimation(self, factor: int = 20):
    points = self.get_points()
    decimated_points = points[::factor]
    return self._gpd_helper.get_dep_points(decimated_points)

  def get_voxel_grid(self, points, voxel_size: float):
    nb_vox = np.ceil((np.max(points, axis=0)
                     - np.min(points, axis=0)) / voxel_size)
    non_empty_voxel_keys, inverse, nb_pts_per_voxel = np.unique(
        ((points - np.min(points, axis=0)) // voxel_size).astype(int), axis=0, return_inverse=True, return_counts=True)
    idx_pts_vox_sorted = np.argsort(inverse)
    return nb_vox, non_empty_voxel_keys, nb_pts_per_voxel, idx_pts_vox_sorted

  def grid_barycenter(self, voxel_size: int):
    last_seen = 0
    voxel_grid = {}
    grid_barycenter = []
    points = self.get_points()
    nb_vox, non_empty_voxel_keys, nb_pts_per_voxel, idx_pts_vox_sorted = self.get_voxel_grid(points, voxel_size)

    for idx, vox in enumerate(non_empty_voxel_keys):
      voxel_grid[tuple(vox)] = points[idx_pts_vox_sorted[last_seen:last_seen + nb_pts_per_voxel[idx]]]
      grid_barycenter.append(np.mean(voxel_grid[tuple(vox)], axis=0))
      last_seen += nb_pts_per_voxel[idx]
    sample_points = np.array(list(map(list, grid_barycenter)))
    return self._gpd_helper.get_dep_points(sample_points)

  def grid_candidate_center(self, voxel_size: int):
      last_seen = 0
      voxel_grid = {}
      grid_candidate_center = []
      points = self.get_points()
      nb_vox, non_empty_voxel_keys, nb_pts_per_voxel, idx_pts_vox_sorted = self.get_voxel_grid(points, voxel_size)

      for idx, vox in enumerate(non_empty_voxel_keys):
        voxel_grid[tuple(
          vox)] = points[idx_pts_vox_sorted[last_seen:last_seen + nb_pts_per_voxel[idx]]]
        grid_candidate_center.append(voxel_grid[tuple(vox)][np.linalg.norm(
          voxel_grid[tuple(vox)] - np.mean(voxel_grid[tuple(vox)], axis=0), axis=1).argmin()])
        last_seen += nb_pts_per_voxel[idx]

      sample_points = np.array(list(map(list, grid_candidate_center)))
      return self._gpd_helper.get_dep_points(sample_points)
