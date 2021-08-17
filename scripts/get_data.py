import json
import pdal

REGION = "IA_FullState"
BOUND = "([-10425171.940, -10423171.940], [5164494.710, 5166494.710])"
PUBLIC_DATA_PATH = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
PIPELINE_PATH = "./get_data.json"


def get_raster_terrain(
    bounds: str = BOUND,
    regions: str = REGION,
    output_filename: str = "temp",
    public_access_path: str = PUBLIC_DATA_PATH,
) -> None:
  with open(PIPELINE_PATH) as js:
    pipe = json.load(js)

  pipe['pipeline'][0]['bounds'] = bounds
  pipe['pipeline'][0]['filename'] = public_access_path + regions + "/ept.json"
  pipe['pipeline'][3]['filename'] = "../data/laz/" + output_filename + ".laz"
  pipe['pipeline'][4]['filename'] = "../data/tif/" + output_filename + ".tif"

  pl = pdal.Pipeline(json.dumps(pipe))

  try:
    pl.execute()
    metadata = pl.metadata
    print('metadata: ', metadata)
    log = pl.log
    print("logs: ", log)
  except RuntimeError as e:
    print(e)


get_raster_terrain()