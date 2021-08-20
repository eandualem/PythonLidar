import json
import pdal
from bounds import Bounds
from config import Config
from log import get_logger
from df_generator import DfGenerator
from file_handler import FileHandler
from shapely.geometry import Polygon


PUBLIC_DATA_PATH = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"


class GetData:
  def __init__(self,
               epsg=26915,
               public_access_path: str = PUBLIC_DATA_PATH,
               metadata_filename: str = "",
               ):
    self._input_epsg = 3857
    self.output_epsg = epsg
    self._public_access_path = public_access_path
    self._df_generator = DfGenerator(self._input_epsg, self.output_epsg)
    self._file_handler = FileHandler()
    self._logger = get_logger("GetData")
    self._metadata = self._file_handler.read_csv(metadata_filename)

  def get_pipeline(self, bounds, polygon_str, regions, filename):
    pipe = self._file_handler.read_json("usgs_3dep_pipeline")

    pipe['pipeline'][0]['filename'] = self._public_access_path + regions + "/ept.json"
    pipe['pipeline'][0]['bounds'] = bounds
    pipe['pipeline'][1]['polygon'] = polygon_str
    pipe['pipeline'][4]['out_srs'] = f'EPSG:{self.output_epsg}'
    pipe['pipeline'][5]['filename'] = str(Config.LAZ_PATH / str(filename + ".laz"))
    pipe['pipeline'][6]['filename'] = str(Config.LAZ_PATH / str(filename + ".tif"))
    return pdal.Pipeline(json.dumps(pipe))

  def check_cache(self):
    # TODO:
    pass

  def get_bound_metadata(self, bounds: Bounds):

    filtered_df = self._metadata.loc[
        (self._metadata['xmin'] <= bounds.xmin)
        & (self._metadata['xmax'] >= bounds.xmax)
        & (self._metadata['ymin'] <= bounds.ymin)
        & (self._metadata['ymax'] >= bounds.ymax)
    ]
    return filtered_df[["filename", "region", "year"]]

  def get_geo_data(self, bounds: Bounds, polygon_str, region) -> None:
      # TODO: check in chache first
    filename = region + "_" + bounds.get_bound_name()
    pl = self.get_pipeline(bounds.get_bound_str(), polygon_str, region, filename)
    try:
      pl.execute()
      geo_data = self._df_generator.get_geo_data(filename)
      self._logger.info(f"successfully read geo data: {filename}")
      return geo_data
    except RuntimeError as e:
      self._logger.exception(f"error reading geo data, error: {e}")

  def get_data(self, polygon: Polygon, region: str = "") -> None:

    bound, polygon_str = self._df_generator.get_bound_from_polygon(polygon)
    if region != "":
      geo_data = self.get_geo_data(bound, polygon_str, region)
      return [geo_data]
    else:
      df_meta = self.get_bound_metadata(bound)
      list_geo_data = []
      for index, row in df_meta.iterrows():

        region = row['filename'].replace('/', '')
        data = self.get_geo_data(bound, polygon_str, region)
        list_geo_data.append(data)

    return list_geo_data


# Test
if __name__ == "__main__":
    fetcher = GetData(epsg=4326, metadata_filename="usgs_3dep_metadata")
    MINX, MINY, MAXX, MAXY = [-93.756155, 41.918015, -93.747334, 41.921429]

    polygon = Polygon(((MINX, MINY), (MINX, MAXY),
                       (MAXX, MAXY), (MAXX, MINY), (MINX, MINY)))

    fetcher.get_data(polygon, "IA_FullState")
