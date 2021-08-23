import os
import sys
from shapely.geometry import Polygon
sys.path.append(os.path.abspath(os.path.join('../scripts')))
from fetch_lidar import FetchLidar


if __name__ == "__main__":
    pass
    fetcher = FetchLidar(epsg=4326, metadata_filename="usgs_3dep_metadata")
    MINX, MINY, MAXX, MAXY = [-93.756155, 41.918015, -93.747334, 41.921429]

    polygon = Polygon(((MINX, MINY), (MINX, MAXY),
                       (MAXX, MAXY), (MAXX, MINY), (MINX, MINY)))

    fetcher.get_data(polygon, ["IA_FullState"])
