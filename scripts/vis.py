import os
import elevation
import matplotlib
import numpy as np
import richdem as rd
import geopandas as gpd
import matplotlib.pyplot as plt


class Vis:
  """Visualizes geospecial data
  """

  def __init__(self, df: gpd.GeoDataFrame):
    self.df = df

  def get_points(self):
    """ Generate numpy array of points from point clouds data.
    """
    x = self.df.geometry.x
    y = self.df.geometry.y
    z = self.df.elevation
    return np.array([x, y, z]).transpose()

  def plot_raster(self, raster_data, title: str = '') -> None:
    """ Plots raster tif image both in log scale(+1) and original version

    Args:
        raster_data ([type]): [description]
        title (str, optional): [description]. Defaults to ''.
    """

    fig, (axlog, axorg) = plt.subplots(1, 2, figsize=(14, 7))
    im1 = axlog.imshow(np.log1p(raster_data))  # vmin=0, vmax=2.1)
#     im2 = axorg.imshow(rast_data)

    plt.title("{}".format(title), fontdict={'fontsize': 15})
    plt.axis('off')
    plt.colorbar(im1, fraction=0.03)
    plt.show()

  def render_3d(self, s: float = 0.01, color: str = "blue") -> None:
    """Plots a 3D terrain scatter plot for the cloud datapoints of geopandas dataframe using matplotlib

    Args:
        df (gpd.GeoDataFrame): [description]
        s (float, optional): [description]. Defaults to 0.01.
        color (str, optional): [description]. Defaults to "blue".
    """
    points = self.get_points()

    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax = plt.axes(projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=0.01, color=color)
    plt.show()

  def plot_heatmap(self, cmap: str = "terrain") -> None:
    """Plots a 2D heat map for the point cloud data using matplotlib

    Args:
        df (gpd.GeoDataFrame): [description]
        cmap (str, optional): [description]. Defaults to "terrain".
    """

    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    self.df.plot(column='elevation', ax=ax, legend=True, cmap=cmap)
    plt.show()
