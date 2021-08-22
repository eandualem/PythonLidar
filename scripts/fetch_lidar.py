import pdal
import json
import pandas as pd
import geopandas as gpd
from bounds import Bounds
from config import Config
from log import get_logger
from shapely.geometry import Polygon
from file_handler import FileHandler
from gpd_helper import GPDHelper


class FetchLidar:
  """ Class for fetching point cloud data from the EPT resource on AWS.
      The class uses PDAL pipeline object for fetching data, 
      For more details on how pipelines are defined see http://www.pdal.io/pipeline.html
  """

  def __init__(self, epsg: int = 26915):
    """ Method used for instantiating the FetchLidar class

    Args:
        epsg (int, optional): Input coordinate reference system. Defaults to 26915.
    """
    self._input_epsg = 3857
    self.output_epsg = epsg
    self._file_handler = FileHandler()
    self._logger = get_logger("GetData")
    self._metadata = self._file_handler.read_csv("usgs_3dep_metadata")
    self._gdf_helper = GPDHelper(self._input_epsg, self.output_epsg)

  def get_pipeline(self, bounds: str, polygon_str: str, region: str, filename: str):
    """ Loads Pipeline template from json file and 
        Updates the pipeline json for fetching point cloud data using pdal

    Args:
        bounds (str): geometry object describing boundary of interest for fetching point cloud data
        polygon_str (str): geometry object describing polygon for croping fetched point cloud data
        region (str): point cloud data resource location
        filename ([str]): name of raster data to be saved

    Returns:
        pdal pipeline object
    """
    pipe = self._file_handler.read_json("usgs_3dep_pipeline")
    pipe['pipeline'][0]['filename'] = Config.USGS_3DEP_PUBLIC_DATA_PATH + \
      region + "/ept.json"
    pipe['pipeline'][0]['bounds'] = bounds
    pipe['pipeline'][1]['polygon'] = polygon_str
    pipe['pipeline'][6]['out_srs'] = f'EPSG:{self.output_epsg}'
    pipe['pipeline'][7]['filename'] = str(Config.LAZ_PATH / str(filename + ".laz"))
    pipe['pipeline'][8]['filename'] = str(Config.TIF_PATH / str(filename + ".tif"))
    return pdal.Pipeline(json.dumps(pipe))

  def get_bound_metadata(self, bounds: Bounds) -> pd.DataFrame:
    """ Filter resource metadata and return dataframes containing the bound points within

    Args:
        bounds (Bounds): geometry object describing boundary of interest for fetching point cloud data

    Returns:
        pd.DataFrame: resource metadata enclosing the given boundary
    """

    filtered_df = self._metadata.loc[
      (self._metadata['xmin'] <= bounds.xmin)
      & (self._metadata['xmax'] >= bounds.xmax)
      & (self._metadata['ymin'] <= bounds.ymin)
      & (self._metadata['ymax'] >= bounds.ymax)
    ]
    return filtered_df[["filename", "region", "year"]]

  def check_valid_bound(self, bounds: Bounds, regions: list) -> bool:
    """ Check if resource boundaries enclose the given boundary. 
        Checks whether region provided inclosed a given boundary.

    Args:
        bounds (Bounds): geometry object describing boundary of interest for fetching point cloud data
        regions (list): point cloud data resource location

    Returns:
        bool: true if all the regions inclose the boundary of interest, otherwise returns false
    """

    for _, row in regions.iterrows():
      cond = (row['xmin'] <= bounds.xmin) & (row['xmax'] >= bounds.xmax) & (
        row['ymin'] <= bounds.ymin) & (row['ymax'] >= bounds.ymax)
      if cond is False:
        return False

    return True

  def get_dep(self, bounds: Bounds, polygon_str: str, region: list) -> gpd.GeoDataFrame:
    """ Excutes pdal pipeline and fetches point cloud data from public repository.
        Using GDfGenerator class creates geopandas dataframe containing geometry and 
        elivation from polygon fetched point cloud data.

    Args:
        bounds (Bounds): geometry object describing boundary of interest
        polygon_str (str): geometry object describing polygon for croping fetched point cloud data
        region (list): point cloud data resource location

    Returns:
        gpd.GeoDataFrame: geopandas dataframe containing geometry and elivation
    """
    filename = region + "_" + bounds.get_bound_name()
    pl = self.get_pipeline(bounds.get_bound_str(),
                           polygon_str, region, filename)
    try:
      pl.execute()
      dep_data = self._gdf_helper.get_dep(pl.arrays)
      self._logger.info(f"successfully read geo data: {filename}")
      return dep_data
    except RuntimeError as e:
      self._logger.exception(f"error reading geo data, error: {e}")

  def fetch_lidar_data(self, polygon: Polygon, regions: list) -> list:
    """ Fetches lidar point cloud data from usgs 3dep public repository in aws

    Args:
        polygon (Polygon): geometry object describing polygon for croping fetched point cloud data
        regions (list): point cloud data resource location

    Returns:
        list: list of geopandas dataframe for all resource location with point cloud data
    """

    bound, polygon_str = self._gdf_helper.get_bound_from_polygon(polygon)

    if len(regions) == 0:
      regions = self.get_bound_metadata(bound)

    else:
      regions = self._metadata[self._metadata['filename'].isin(regions)]
      if self.check_valid_bound(bound, regions) is False:
        self._logger.exception("The boundary is not within the region provided")

    list_geo_data = []
    for index, row in regions.iterrows():
      try:
        data = self.get_dep(bound, polygon_str, row['filename'])

        if(data is not None):
          list_geo_data.append({'year': row['year'],
                                'region': row['region'],
                                'geo_data': data,
                                })

      except RuntimeError as e:
        self._logger.exception(
          f"error featching geo data for {row['filename']}, error: {e}")
    return list_geo_data
