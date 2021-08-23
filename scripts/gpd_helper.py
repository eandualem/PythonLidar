import numpy as np
import geopandas as gpd
from bounds import Bounds
from log import get_logger
from file_handler import FileHandler
from shapely.geometry import Point, Polygon


class GPDHelper:
  """ A helper class that uses GeoPandas (a python library for working with geospatial data) 
      and provides simple functionalities for other classes.
  """

  def __init__(self, input_epsg:int, output_epsg:int) -> None:
    """ 
    Args:
        input_epsg (int): Coordinate reference system for use in transformations.
        output_epsg (int): A coordinate reference system that the user uses.
    """
    self.input_epsg = input_epsg
    self.output_epsg = output_epsg
    self._file_handler = FileHandler()
    self._logger = get_logger("DfGenerator")

  def covert_crs(self, df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """ Transform geometries to a new coordinate reference system.

    Args:
        df (gpd.GeoDataFrame): A geopandas dataframe. The CRS attributes on the GeoSeries that's are to be transformed must be set.

    Returns:
        gpd.GeoDataFrame
    """
    df['geometry'] = df['geometry'].to_crs(self.output_epsg)
    df = df.set_crs(self.output_epsg)
    return df

  def get_dep_points(self, array_of_points: np.ndarray) -> gpd.GeoDataFrame:
    """ Constructs a Geopandas data frame having an elevation column and a geometry column representing point cloud data in a given coordinate reference system.

    Args:
        array_data (np.ndarray): A point cloud data from pdal pipeline

    Returns:
        gpd.GeoDataFrame: A geopandas data frame containing geometry and elevation.
    """
    
    geometry_points = [Point(x, y) for x, y in zip(array_of_points[:, 0], array_of_points[:, 1])]
    elevations = np.array(array_of_points[:, 2])

    df = gpd.GeoDataFrame(columns=["elevation", "geometry"])
    df['elevation'] = elevations
    df['geometry'] = geometry_points
    df = df.set_geometry("geometry")
    df.set_crs(epsg=self.output_epsg, inplace=True)
    return df

  def get_dep(self, array_data: np.ndarray) -> gpd.GeoDataFrame:
    """ Constructs a Geopandas data frame having an elevation column 
        and a geometry column representing point cloud data in a given coordinate reference system.

    Args:
        array_data (np.ndarray): A point cloud data in a numpy format

    Returns:
        gpd.GeoDataFrame: A geopandas data frame containing geometry and elevation.
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
    """ Compute Polygons Cropping string used when building Pdal crop pipeline.

    Args:
        x_cord: LinearRings is the outer boundary limit in the GeoSeries in the longitudinal direction.
        y_cord: LinearRings is the outer boundary limit in the GeoSeries in the latitude direction.

    Returns:
        str: A string of a given polygon in a form accepted by the pdal pipeline.
    """
    polygon_str = 'POLYGON(('
    for x, y in zip(list(x_cord), list(y_cord)):
      polygon_str += f'{x} {y}, '
    polygon_str = polygon_str[:-2]
    polygon_str += '))'
    return polygon_str

  def get_bound_from_polygon(self, polygon: Polygon) -> tuple:
    """ Computes bounds value for the given polygon

    Args:
        polygon (Polygon): Shapely geometry object describing the polygon.

    Returns:
        tuple: A tuple of Bounds object and a string of a given polygon in a form accepted by the pdal pipeline.
    """
    polygon_df = gpd.GeoDataFrame([polygon], columns=['geometry'])
    polygon_df.set_crs(epsg=self.output_epsg, inplace=True)
    polygon_df['geometry'] = polygon_df['geometry'].to_crs(epsg=self.input_epsg)
    xmin, ymin, xmax, ymax = polygon_df['geometry'][0].bounds
    bound = Bounds(xmin, xmax, ymin, ymax)
    x_cord, y_cord = polygon_df['geometry'][0].exterior.coords.xy
    polygon_str = self.get_polygon_str(x_cord, y_cord)
    return bound, polygon_str
