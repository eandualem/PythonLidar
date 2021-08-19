import numpy as np
from log import get_logger
from file_handler import FileHandler
import geopandas as gpd
from shapely.geometry import box, Point, Polygon


class ElevationExtractor:
  def __init__(self,
               filename: str = "temp",
               crs_epgs=26915) -> None:
    self.filename = filename
    self.crs_epgs = crs_epgs
    self._file_handler = FileHandler()
    self._logger = get_logger("ElevationExtractor")

  def get_elevation(self):
    las = self._file_handler(self.filename)
    geometry_points = [Point(x, y) for x, y in zip(las.x, las.y)]
    elevations = np.array(las.z)

    df = gpd.GeoDataFrame(columns=["elevation", "geometry"])
    df['elevation'] = elevations
    df['geometry'] = geometry_points
    df = df.set_geometry("geometry")
    df.set_crs(epsg=self.crs_epgs, inplace=True)
    return df

  def covert_crs(self, crs_epgs: int, df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    df['geometry'] = df['geometry'].to_crs(crs_epgs)
    return df
