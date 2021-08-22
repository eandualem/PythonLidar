import numpy as np
import geopandas as gpd
from bounds import Bounds
from log import get_logger
from file_handler import FileHandler
from shapely.geometry import box, Point, Polygon


class GPDHelper:
  """ The class contains helper functions that uses GeoPandas, a python library for working with
      geospatial data, and provide different functionalities.
  """

  def __init__(self, input_epsg, output_epsg) -> None:
    """ Method used for instantiating the GPDHelper class

    Args:
        input_epsg ([type]): [description]
        output_epsg ([type]): [description]
    """
    self.output_epsg = output_epsg
    self.input_epsg = input_epsg
    self._file_handler = FileHandler()
    self._logger = get_logger("DfGenerator")

  def covert_crs(self, crs_epgs: int, df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """ Transform geometries to a new coordinate reference system.

    Args:
        crs_epgs (int): Coordinate reference system to be used for transformation
        df (gpd.GeoDataFrame): A geopandas dataframe. The crs attribute on the GeoSeries thats is to be transformed must be set.

    Returns:
        gpd.GeoDataFrame
    """
    df['geometry'] = df['geometry'].to_crs(crs_epgs)
    return df

  def get_dep(self, array_data: np.ndarray) -> gpd.GeoDataFrame:
    """ constructs a geopandas data frame having an elevation column and a geometry column representing point coordinates in a given coordinate reference system
        from point cloud data.

    Args:
        array_data (np.ndarray): point cloud data from  pdal pipeline

    Returns:
        [type]: geopandas dataframe containing geometry and elivation
    """
    for i in array_data:
      geometry_points = [Point(x, y) for x, y in zip(i["X"], i["Y"])]
      elevations = np.array(i["Z"])

      df = gpd.GeoDataFrame(columns=["elevation", "geometry"])
      df['elevation'] = elevations
      df['geometry'] = geometry_points
      df = df.set_geometry("geometry")
      df.set_crs(epsg=self.output_epsg, inplace=True)
    return df

  def get_polygon_str(self, x_cord, y_cord) -> str:
    """ Compute Polygons Cropping string used when building Pdal's crop pipeline.

    Args:
        x_cord: [description]
        y_cord: [description]

    Returns:
        str: [description]
    """
    polygon_str = 'POLYGON(('
    for x, y in zip(list(x_cord), list(y_cord)):
      polygon_str += f'{x} {y}, '
    polygon_str = polygon_str[:-2]
    polygon_str += '))'
    return polygon_str

  def get_bound_from_polygon(self, polygon: Polygon) -> tuple:
    """ computes bounds value for the given polygon

    Args:
        polygon (Polygon): shapely geometry object describing polygon

    Returns:
        tuple: returns a tuple of Bounds object and 
    """
    polygon_df = gpd.GeoDataFrame([polygon], columns=['geometry'])
    polygon_df.set_crs(epsg=self.output_epsg, inplace=True)
    polygon_df['geometry'] = polygon_df['geometry'].to_crs(epsg=self.input_epsg)
    xmin, ymin, xmax, ymax = polygon_df['geometry'][0].bounds
    bound = Bounds(xmin, xmax, ymin, ymax)
    x_cord, y_cord = polygon_df['geometry'][0].exterior.coords.xy
    polygon_str = self.get_polygon_str(x_cord, y_cord)
    return bound, polygon_str
