import json
import urllib3
import pandas as pd
from log import get_logger
from file_handler import FileHandler

DEFAULT_URL = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
DEFAULT_FILENAME = "usgs_3dep_filenames"


class GetMetadata():

  def __init__(self, name: str = DEFAULT_FILENAME, target_url: str = DEFAULT_URL):
    self.url = target_url
    self.filename = name
    self._http = urllib3.PoolManager()
    self._file_handler = FileHandler()
    self._logger = get_logger("GetMetadata")

  def get_metadata(self):
    filenames = self.file_handler.read_txt(self.name)
    df = pd.DataFrame(columns=['dataset', 'xmin', 'xmax', 'ymin', 'ymax', 'points'])
  
    index = 0
    for d in filenames:
      r = self.http.request('GET', self.url + d + "ept.json")
      if r.status == 200:
        j = json.loads(r.data)
        df = df.append({
          'dataset': d,
          'xmin': j['bounds'][0],
          'xmax': j['bounds'][3],
          'ymin': j['bounds'][1],
          'ymax': j['bounds'][4],
          'points': j['points']}, ignore_index=True)

        if(index % 100 == 0):
          print(f"Read progress: {((index / len(filenames)) * 100):.2f}%")
        index += 1
      else:
        self.logger.exception(f"Connection problem at index: {((index / len(filenames)) * 100):.2f}%")
        return
    self._file_handler.save_csv(df, self.filename)
