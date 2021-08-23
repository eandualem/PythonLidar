from vis import Vis
import geopandas as gpd
from fetch_lidar import FetchLidar
from sub_sampler import SubSampler
from shapely.geometry import Polygon
from fcache.cache import FileCache


class PythonLidar:
  """ PythonLidar is an open-source python package for retrieving, transforming, and visualizing point cloud data obtained through an aerial LiDAR survey. Using the package, you can select a region of interest, and download the related point cloud dataset with its metadata in different file formats (.laz, .tif, or as an ASCII file), perform transformation and visualization using the downloaded data.
  """
  def __init__(self, epsg=26915):
    self.output_epsg = epsg
    self._input_epsg = 3857
    self._fetch_lidar = FetchLidar(self.output_epsg)
    self._cache = FileCache('PythonLidar')

  def fetch_lidar(self, polygon: Polygon, regions=[]):
    return self._fetch_lidar.fetch_lidar_data(polygon, regions)

  def get_renderer(self, df: gpd.GeoDataFrame) -> Vis:
    return Vis(df)

  def get_sub_sampler(self, epsg, df: gpd.GeoDataFrame) -> SubSampler:
    return SubSampler(self._input_epsg, epsg, df)

