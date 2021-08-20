from pathlib import Path


class Config:
  RANDOM_SEED = 27
  ROOT_PATH = Path("./")
  REPO = "https://github.com/eandualem/PythonLidar"
  LOG_FILE = ROOT_PATH / "log/PythonLidara.log"
  DATA_PATH = ROOT_PATH / "data/"
  ASSETS_PATH = ROOT_PATH / "assets/"
  LAZ_PATH = DATA_PATH / "laz"
  TIF_PATH = DATA_PATH / "shp"
  SHP_PATH = DATA_PATH / "tif"
  IMG_PATH = DATA_PATH / "img"
