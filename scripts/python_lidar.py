from bounds import Bounds
from config import Config
from log import get_logger
from fetch_lidar import FetchLidar
from file_handler import FileHandler
from get_metadata import GetMetadata
from df_generator import DfGenerator
from shapely.geometry import Polygon
from fcache.cache import FileCache


class PythonLidar:
  def __init__(self, epsg=26915):
    self.output_epsg = epsg
    self._input_epsg = 3857
    self._fetch_lidar = FetchLidar(self.output_epsg)
    self._cache = FileCache('PythonLidar')

  def check_in_chache(self, bound_str: str):
    pass

  def fetch_lidar(self, polygon: Polygon, regions=[]):
    # TODO: Check in cache
    
