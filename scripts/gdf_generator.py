import numpy as np
import geopandas as gpd
from bounds import Bounds
from log import get_logger
from file_handler import FileHandler
from shapely.geometry import box, Point, Polygon


class GDfGenerator:
  def __init__(self, input_epsg, output_epsg) -> None:
    self.output_epsg = output_epsg
    self.input_epsg = input_epsg
    self._file_handler = FileHandler()
    self._logger = get_logger("DfGenerator")

  def get_dep(self, array_data):
    for i in array_data:
      geometry_points = [Point(x, y) for x, y in zip(i["X"], i["Y"])]
      elevations = np.array(i["Z"])

      df = gpd.GeoDataFrame(columns=["elevation", "geometry"])
      df['elevation'] = elevations
      df['geometry'] = geometry_points
      df = df.set_geometry("geometry")
      df.set_crs(epsg=self.output_epsg, inplace=True)
    return df

  def covert_crs(self, crs_epgs: int, df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    df['geometry'] = df['geometry'].to_crs(crs_epgs)
    return df

  def get_polygon_str(self, x_cord, y_cord):
    polygon_str = 'POLYGON(('
    for x, y in zip(list(x_cord), list(y_cord)):
      polygon_str += f'{x} {y}, '
    polygon_str = polygon_str[:-2]
    polygon_str += '))'
    return polygon_str

  def get_bound_from_polygon(self, polygon: Polygon):
    polygon_df = gpd.GeoDataFrame([polygon], columns=['geometry'])
    polygon_df.set_crs(epsg=self.output_epsg, inplace=True)
    polygon_df['geometry'] = polygon_df['geometry'].to_crs(epsg=self.input_epsg)
    xmin, ymin, xmax, ymax = polygon_df['geometry'][0].bounds
    bound = Bounds(xmin, xmax, ymin, ymax)
    x_cord, y_cord = polygon_df['geometry'][0].exterior.coords.xy
    polygon_str = self.get_polygon_str(x_cord, y_cord)
    return bound, polygon_str
