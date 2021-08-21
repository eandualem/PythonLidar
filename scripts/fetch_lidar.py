import json
import pickle
from numpy import empty
from pandas.core.indexes.base import ensure_index
import pdal
from bounds import Bounds
from config import Config
from log import get_logger
from gdf_generator import GDfGenerator
from file_handler import FileHandler
from shapely.geometry import Polygon
import geopandas as gpd


class FetchLidar:
  """[summary]
  """

  def __init__(self, epsg: int = 26915):
    """[summary]

    Args:
        epsg (int, optional): [description]. Defaults to 26915.
    """
    self._input_epsg = 3857
    self.output_epsg = epsg
    self._file_handler = FileHandler()
    self._logger = get_logger("GetData")
    self._metadata = self._file_handler.read_csv("usgs_3dep_metadata")
    self._gdf_generator = GDfGenerator(self._input_epsg, self.output_epsg)

  def get_pipeline(self, bounds: str, polygon_str: str, region: str, filename):
    pipe = self._file_handler.read_json("usgs_3dep_pipeline")
    pipe['pipeline'][0]['filename'] = Config.USGS_3DEP_PUBLIC_DATA_PATH + \
      region + "/ept.json"
    pipe['pipeline'][0]['bounds'] = bounds
    pipe['pipeline'][1]['polygon'] = polygon_str
    pipe['pipeline'][4]['out_srs'] = f'EPSG:{self.output_epsg}'
    # pipe['pipeline'][5]['filename'] = str(Config.LAZ_PATH / str(filename + ".laz"))
    # pipe['pipeline'][6]['filename'] = str(Config.TIF_PATH / str(filename + ".tif"))
    return pdal.Pipeline(json.dumps(pipe))

  def get_bound_metadata(self, bounds: Bounds):

    filtered_df = self._metadata.loc[
        (self._metadata['xmin'] <= bounds.xmin)
        & (self._metadata['xmax'] >= bounds.xmax)
        & (self._metadata['ymin'] <= bounds.ymin)
        & (self._metadata['ymax'] >= bounds.ymax)
    ]
    return filtered_df[["filename", "region", "year"]]

  def check_valid_bound(self, bounds: Bounds, regions: list):
    for index, row in regions.iterrows():
      cond = (row['xmin'] <= bounds.xmin) & (row['xmax'] >= bounds.xmax) & (
        row['ymin'] <= bounds.ymin) & (row['ymax'] >= bounds.ymax)
      if cond is False:
        return False

    return True

  def get_geo_data(self, bounds: Bounds, polygon_str: str, region: list) -> gpd.GeoDataFrame:
    filename = region + "_" + bounds.get_bound_name()
    pl = self.get_pipeline(bounds.get_bound_str(),
                           polygon_str, region, filename)
    try:
      pl.execute()
      dep_data = self._gdf_generator.get_dep(pl.arrays)
      self._logger.info(f"successfully read geo data: {filename}")
      return dep_data
    except RuntimeError as e:
      self._logger.exception(f"error reading geo data, error: {e}")

  def fetch_lidar_data(self, polygon: Polygon, regions: list) -> list:

    bound, polygon_str = self._gdf_generator.get_bound_from_polygon(polygon)
    if len(regions) == 0:
      regions = self.get_bound_metadata(bound)
    else:
      regions = self._metadata[self._metadata['filename'].isin(regions)]
      if self.check_valid_bound(bound, regions) is False:
        self._logger.exception("The boundary is not within the region provided")
    print(regions)
    list_geo_data = []
    for index, row in regions.iterrows():
      try:
        data = self.get_geo_data(bound, polygon_str, row['filename'])
        list_geo_data.append({'year': row['year'],
                              'region': row['region'],
                              'geo_data': data,
                              })
      except RuntimeError as e:
        self._logger.exception(
          f"error featching geo data for {row['filename']}, error: {e}")
    return list_geo_data
