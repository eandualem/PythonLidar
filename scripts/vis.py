import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt


class Vis:
  """ This class is used for Visualizing geospatial data
  """

  def __init__(self, df: gpd.GeoDataFrame):
    self.df = df

  def get_points(self):
    """ Generates a NumPy array from point clouds data.
    """
    x = self.df.geometry.x
    y = self.df.geometry.y
    z = self.df.elevation
    return np.array([x, y, z]).transpose()

  def plot_raster(self, raster_data, title: str = '') -> None:
    """ Plots raster tif image both in log scale(+1) and original version
    """

    fig, (axlog, axorg) = plt.subplots(1, 2, figsize=(14, 7))
    im1 = axlog.imshow(np.log1p(raster_data))  # vmin=0, vmax=2.1)
#     im2 = axorg.imshow(rast_data)

    plt.title("{}".format(title), fontdict={'fontsize': 15})
    plt.axis('off')
    plt.colorbar(im1, fraction=0.03)
    plt.show()

  def render_3d(self, s: float = 0.01, color: str = "blue") -> None:
    """ Plots a 3D terrain scatter plot for the cloud data points of geopandas data frame using matplotlib
    """
    points = self.get_points()

    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    ax = plt.axes(projection='3d')
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=0.01, color=color)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Elivation')
    plt.show()

  def plot_heatmap(self, title) -> None:
    """ Plots a 2D heat map for the point cloud data using matplotlib
    """

    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    fig.patch.set_alpha(0)
    plt.grid('on', zorder=0)
    self.df.plot(column='elevation', ax=ax, legend=True, cmap="terrain")
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()
