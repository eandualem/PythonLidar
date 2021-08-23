import re
import json
import urllib3
import pandas as pd
from log import get_logger
from file_handler import FileHandler

DEFAULT_URL = "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/"
DEFAULT_FILENAME = "usgs_3dep_filenames"


class GetMetadata():
  """ Generates metadata describing the region, year, xmin, xmax, ymin, ymax, 
      and amount of point cloud data for all EPT resources on AWS. 
  """

  def __init__(self, name: str = DEFAULT_FILENAME, target_url: str = DEFAULT_URL):
    """ 
    Args:
        name (str, optional): Name of a file that contains all EPT resource locations on AWS. Defaults to DEFAULT_FILENAME.
        target_url (str, optional): A url containing the ept resource file. Defaults to DEFAULT_URL.
    """
    self.url = target_url
    self.filename = name
    self._http = urllib3.PoolManager()
    self._file_handler = FileHandler()
    self._logger = get_logger("GetMetadata")

  def get_name_and_year(self, resource_location: str) -> tuple:
    """ Extracts year and region from EPT resource location.

    Args:
        resource_location (str): Name of EPT resource location 

    Returns:
        tuple: A tuple containing the name of the region and year
    """

    resource_location = resource_location.replace('/', '')
    regex = '20[0-9][0-9]+'
    match = re.search(regex, resource_location)
    if(match):
      return (resource_location[:match.start() - 1], resource_location[match.start():match.end()])
    else:
      return (resource_location, None)

  def get_metadata(self):
    """ Extracts metadata for all EPT resources on AWS
    """
    filenames = self._file_handler.read_txt(self.filename)
    df = pd.DataFrame(columns=['filename', 'region',
                      'year', 'xmin', 'xmax', 'ymin', 'ymax', 'points'])

    index = 0
    for f in filenames:
      r = self._http.request('GET', self.url + f + "ept.json")
      if r.status == 200:
        j = json.loads(r.data)
        region, year = self.get_name_and_year(f)

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
