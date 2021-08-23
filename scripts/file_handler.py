import json
import laspy
import pandas as pd
from config import Config
from log import get_logger


class FileHandler():
  """ Read and save files in different file format
  """

  def __init__(self):
    self._logger = get_logger("FileHandler")

  def save_csv(self, df: pd.DataFrame, name: str, index: bool = False) -> None:
    """ Saves CSV file to disk

    Args:
        df (pd.DataFrame): pandas data frame to be saved
        name (str): The name of the file to be stored.
        index (bool, optional): Whether to keep index column or not. Defaults to False.
    """

    try:
      path = Config.ASSETS_PATH / str(name + '.csv')
      df.to_csv(path, index=index)
      self._logger.info(f"{name} is saved successfully in csv format")
    except Exception:
      self._logger.exception(f"{name} save failed")

  def read_csv(self, name: str, missing_values=[]) -> pd.DataFrame:
    """ Reads CSV file from disk into a pandas data frame

    Args:
        name (str): The name of the file to read.
        missing_values (list, optional): values that are considered to be None. Defaults to [].

    Returns:
        pd.DataFrame: dataframe
    """
    try:
      path = Config.ASSETS_PATH / str(name + '.csv')
      df = pd.read_csv(path, na_values=missing_values)
      self._logger.info(f"{name} read successfully")
      return df
    except FileNotFoundError:
      self._logger.exception(f"{name} not found")

  def read_json(self, name: str) -> dict:
    """ Reads json file from disk

    Args:
        name (str): The name of the file to read.

    Returns:
        dict: Python dictionary
    """
    try:
      path = Config.ASSETS_PATH / str(name + '.json')
      with open(path, 'r') as json_file:
        json_obj = json.load(json_file)
      self._logger.info(f"{name} read successfully")
      return json_obj
    except Exception:
      self._logger.exception(f"{name} not found")

  def read_txt(self, name: str) -> list:
    """ Reads JSON file from disk

    Args:
        name (str): The name of the file to read.

    Returns:
        list: List of text line by line
    """
    try:
      path = Config.ASSETS_PATH / str(name + '.txt')
      with open(path, "r") as f:
        text_file = f.read().splitlines()
      self._logger.info(f"{name} read successfully")
      return text_file
    except Exception:
      self._logger.exception(f"{name} not found")

  def read_point_data(self, name: str):
    """ Reads laz file from disk

    Args:
        name (str): The name of the file to read.

    Returns:
        raster data
    """
    try:
      path = Config.LAZ_PATH / str(name + '.laz')
      print(path)
      las = laspy.read(path)
      self._logger.info(f"{name} read successfully")
      return las
    except Exception:
      self._logger.exception(f"{name} not found")
