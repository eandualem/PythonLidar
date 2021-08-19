import json
import pdal
from config import Config
from df_generator import DfGenerator
from log import get_logger
from file_handler import FileHandler

PUBLIC_DATA_PATH = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
PIPELINE_PATH = "./get_data.json"


class GetData:
  def __init__(self,
               public_access_path: str = PUBLIC_DATA_PATH,
               metadata_filename: str = "",
               ):
    self._public_access_path = public_access_path
    self._metadata_filename = metadata_filename
    self._df_generator = DfGenerator()
    self._logger = get_logger("FileHandler")
    self._file_handler = FileHandler()

  def get_pipeline(self, bounds, regions, filename):
    pipe = self._file_handler.read_json(PIPELINE_PATH)

    pipe['pipeline'][0]['bounds'] = bounds
    pipe['pipeline'][0]['filename'] = self._public_access_path + regions + "/ept.json"
    pipe['pipeline'][3]['filename'] = "../data/laz/" + filename + ".laz"
    pipe['pipeline'][4]['filename'] = "../data/tif/" + filename + ".tif"
    return pdal.Pipeline(json.dumps(pipe))

  def check_cache(self):
    # TODO:
    pass

  def get_regions(self, bounds: str):
    df = self._file_handler.read_csv(self._metadata_filename)
    filtered_df = df[
      df['xmin'] > bounds[0][0]
      and df['xmax'] > bounds[0][1]
      and df['ymin'] > bounds[1][0]
      and df['ymax'] > bounds[1][1]
    ]
    return filtered_df[["dataset"]]

  def get_geo_data(self, bounds, region, filename) -> None:
    # TODO: check in chache first
    pl = self.get_pipeline(bounds, region, filename)
    try:
      pl.execute()
      # metadata = pl.metadata
      geo_data = self._df_generator.get_geo_data(filename)
      self._logger(f"successfully read geo data: {filename}")
      return geo_data
    except RuntimeError as e:
      self._logger(f"error reading geo data, error: {e}")

  def get_data(self, bounds: str) -> None:
    list_geo_data = []
    for region in self.get_regions():
      filename = region + "_".join(bounds)
      list_geo_data.append(self.get_geo_data(filename))
    return list_geo_data


# Test
get_data = GetData()
get_data.get_raster_terrain(
    bounds="([-10425171.940, -10423171.940], [5164494.710, 5166494.710])",
    regions="IA_FullState",
    output_filename="iowa",
)

# get_data.get_raster_terrain(
#     bounds="([-11669524.7, -11666600.81], [4776607.3, 4778714.4])",
#     regions="USGS_LPC_CO_SoPlatteRiver_Lot5_2013_LAS_2015",
#     output_filename="SoPlatteRiver",
# )
