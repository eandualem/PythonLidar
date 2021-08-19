import json
import pandas as pd
from config import Config
from log import get_logger


class FileHandler():

  def __init__(self):
    self.logger = get_logger("FileHandler")

  def read_json(self, name):
    try:
      path = Config.ASSETS_PATH / str(name + '.json')
      with open(path, 'r') as json_file:
        json_obj = json.load(json_file)
      self.logger.info(f"{name} read successfully")
      return json_obj
    except Exception:
      self.logger.exception(f"{name} not found")

  def save_csv(self, df, name, index=False):
    try:
      path = Config.ASSETS_PATH / str(name + '.csv')
      df.to_csv(path, index=index)
      self.logger.info(f"{name} is saved successfully in csv format")
    except Exception:
      self.logger.exception(f"{name} save failed")

  def read_csv(self, name, missing_values=[]):
    try:
      path = Config.ASSETS_PATH / str(name + '.csv')
      df = pd.read_csv(path, na_values=missing_values)
      self.logger.info(f"{name} read successfully")
      return df
    except FileNotFoundError:
      self.logger.exception(f"{name} not found")
