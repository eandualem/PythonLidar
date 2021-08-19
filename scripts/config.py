from pathlib import Path


class Config:
  RANDOM_SEED = 27
  ROOT_PATH = Path("../")
  REPO = "https://github.com/eandualem/PythonLidar"
  DATA_PATH = ROOT_PATH / "data/"
  ASSETS_PATH = ROOT_PATH / "asset/"
  LAZ_PATH = DATA_PATH / "laz"
  TIF_PATH = DATA_PATH / "shp"
  SHP_PATH = DATA_PATH / "tif"
  IMG_PATH = DATA_PATH / "img"
