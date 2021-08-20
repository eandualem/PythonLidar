import re
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

  def get_name_and_year2(self, filename):
    filename = filename.replace('/', '')
    regex = '20[0-9][0-9]+'
    match = re.search(regex, filename)
    if(match):
      return (filename[:match.start() - 1], filename[match.start():match.end()])
    else:
      return (filename, None)

  def get_metadata(self):
    filenames = self._file_handler.read_txt(self.filename)
    df = pd.DataFrame(columns=['filename', 'region', 'year', 'xmin', 'xmax', 'ymin', 'ymax', 'points'])

    index = 0
    for f in filenames:
      r = self._http.request('GET', self.url + f + "ept.json")
      if r.status == 200:
        j = json.loads(r.data)
        region, year = self.get_name_and_year2(f)

        df = df.append({
          'filename': f.replace('/', ''),
          'region': region,
          'year': year,
          'xmin': j['bounds'][0],
          'xmax': j['bounds'][3],
          'ymin': j['bounds'][1],
          'ymax': j['bounds'][4],
          'points': j['points']}, ignore_index=True)

        if(index % 100 == 0):
          print(f"Read progress: {((index / len(filenames)) * 100):.2f}%")
        index += 1
      else:
        self._logger.exception(f"Connection problem at: {f}")
        # return
    self._file_handler.save_csv(df, "usgs_3dep_metadata")


if __name__ == "__main__":
  gm = GetMetadata()
  gm.get_metadata()
