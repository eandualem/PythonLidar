
import sys
from bounds import Bounds
from config import Config
from log import get_logger
import geopandas as gpd
from fcache.cache import FileCache
from shapely.geometry import Polygon

sys.path.append(os.path.abspath(os.path.join('./scripts')))
from fetch_lidar import FetchLidar
from file_handler import FileHandler
from get_metadata import GetMetadata
from gdf_generator import GDfGenerator


class PythonLidar:
  """PythonLidar is open source python package for retrieving, transforming and visualizing point cloud data.
  """
  def __init__(self, epsg=26915):
    self.output_epsg = epsg
    self._input_epsg = 3857
    self._fetch_lidar = FetchLidar(self.output_epsg)
    self._cache = FileCache('PythonLidar')

  def check_in_chache(self, bound_str: str):
    pass

  def fetch_lidar(self, polygon: Polygon, regions=[]):
    # TODO: Check in cache
    return self._fetch_lidar.fetch_lidar_data(polygon, regions)
