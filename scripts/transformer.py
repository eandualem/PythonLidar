import numpy as np
import richdem as rd
import geopandas as gpd
from pysheds.grid import Grid
import matplotlib.pyplot as plt


class Transformer:

  def __init__(self, path):
    self.grid = Grid.from_raster(path, data_name='dem')
    self.dirmap = (64, 128, 1, 2, 4, 8, 16, 32)

  def get_points(self):
    """ Generate numpy array of points from point clouds data.
    """
    x = self.df.geometry.x
    y = self.df.geometry.y
    z = self.df.elevation
    return np.array([x, y, z]).transpose()

  def compute_flow_direction(self):
    self.grid.resolve_flats('dem', out_name='inflated_dem')
    self.grid.flowdir(data='inflated_dem', out_name='dir', dirmap=self.dirmap)

  def compute_catchment(self, x, y):
    self.grid.catchment(data='dir', x=x, y=y, dirmap=self.dirmap,
                        out_name='catch', recursionlimit=15000, xytype='label')
    self.grid.clip_to('catch')

  def accumulation(self):
    self.grid.accumulation(data='catch', dirmap=self.dirmap, out_name='acc')
