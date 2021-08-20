import json
import pdal
from config import Config
from df_generator import DfGenerator
from log import get_logger
from file_handler import FileHandler
from bounds import Bounds

PUBLIC_DATA_PATH = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"


class GetData:
  def __init__(self,
               public_access_path: str = PUBLIC_DATA_PATH,
               metadata_filename: str = "",
               ):
    self._public_access_path = public_access_path
    self._df_generator = DfGenerator()
    self._logger = get_logger("FileHandler")
    self._file_handler = FileHandler()
    self._metadata = self._file_handler.read_csv(metadata_filename)

  def get_pipeline(self, bounds, regions, filename):
    pipe = self._file_handler.read_json("usgs_3dep_pipeline")

    pipe['pipeline'][0]['bounds'] = bounds
    pipe['pipeline'][0]['filename'] = self._public_access_path + regions + "/ept.json"
    pipe['pipeline'][3]['filename'] = str(Config.LAZ_PATH / str(filename + ".laz"))
    pipe['pipeline'][4]['filename'] = str(Config.LAZ_PATH / str(filename + ".tif"))
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

  def get_geo_data(self, bounds, region, filename) -> None:
    # TODO: check in chache first
    pl = self.get_pipeline(bounds, region, filename)
    try:
      pl.execute()
      geo_data = self._df_generator.get_geo_data(filename)
      self._logger.info(f"successfully read geo data: {filename}")
      return geo_data
    except RuntimeError as e:
      self._logger.exception(f"error reading geo data, error: {e}")

  def get_data(self, bounds: str) -> None:
    list_geo_data = []
    df_meta = self.get_bound_metadata(bounds)
    for index, row in df_meta.iterrows():
      filename = row['filename'].replace('/', '')
      data = self.get_geo_data(bounds.get_bound_str(), filename, filename)
      list_geo_data.append(data)

    return list_geo_data


# Test
bounds = Bounds(-10436887.43333523, -10435905.484106943, 5148706.389047224, 5149217.145836504)
# bounds = Bounds(-10425171.940, -10423171.940, 5164494.710, 5166494.710)
get_data = GetData(metadata_filename="usgs_3dep_metadata")
get_data.get_data(bounds)

# get_data.get_raster_terrain(
#     bounds="([-10425171.940, -10423171.940], [5164494.710, 5166494.710])",
# )

# get_data.get_raster_terrain(
#     bounds="([-11669524.7, -11666600.81], [4776607.3, 4778714.4])",
#     regions="USGS_LPC_CO_SoPlatteRiver_Lot5_2013_LAS_2015",
#     output_filename="SoPlatteRiver",
# )
