import json
import pdal
from config import Config
from log import get_logger
from file_handler import FileHandler

PUBLIC_DATA_PATH = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
PIPELINE_PATH = "./get_data.json"


class GetData:
  def __init__(self,
               output_filename: str = "temp",
               public_access_path: str = PUBLIC_DATA_PATH):
    self._public_access_path = public_access_path
    self._output_filename = output_filename
    self._logger = get_logger("FileHandler")
    self._file_handler = FileHandler()

  def get_pipeline(self, bounds, regions):
    pipe = self._file_handler.read_json(PIPELINE_PATH)

    pipe['pipeline'][0]['bounds'] = bounds
    pipe['pipeline'][0]['filename'] = self._public_access_path + regions + "/ept.json"
    pipe['pipeline'][3]['filename'] = "../data/laz/" + self._output_filename + ".laz"
    pipe['pipeline'][4]['filename'] = "../data/tif/" + self._output_filename + ".tif"
    return pdal.Pipeline(json.dumps(pipe))

  def get_region(self):
    # TODO: dynamically retrieve region
    pass

  def get_raster_terrain(self, bounds: str, regions: str) -> None:
    pl = self.get_pipeline(bounds, regions)

    try:
      pl.execute()
      metadata = pl.metadata
      print('metadata: ', metadata)
      log = pl.log
      print("logs: ", log)
    except RuntimeError as e:
      print(e)


# Test

get_data = GetData()
get_data.get_raster_terrain(
  bounds="([-10425171.940, -10423171.940], [5164494.710, 5166494.710])",
  regions="IA_FullState",
  output_filename="iowa",
)

get_data.get_raster_terrain(
  bounds="([-11669524.7, -11666600.81], [4776607.3, 4778714.4])",
  regions="USGS_LPC_CO_SoPlatteRiver_Lot5_2013_LAS_2015",
  output_filename="SoPlatteRiver",
)
