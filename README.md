# PythonLidar

**Table of content**

- [](#)
- [PythonLidar](#PythonLidar)
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Install](#install)
  - [Data](#data)
  - [Notebooks](#notebooks)
  - [Scripts](#scripts)
  - [Test](#test)

## Overview

PythonLidar is a python package for fetching, manipulating, and visualizing point cloud data. The package will accept boundary polygons in Pandas data frame and return a python dictionary with all years of data available and a geopandas grid point file with elevations encoded in the requested CRS. The package will provide an option to graphically display the returned elevation files as a 3D render plot and heatmap. If possible the package will allow for query and fetch for USGS soil data SSURGO, Satellite data, Climate data and visualize them together with the LIDAR data. There will be a quick start guide for the package with code snippets to help users.

## Requirements
- PDAL
- Laspy
- Geopandas

## Install
```
git clone https://github.com/eandualem/PythonLidar
cd PythonLidar
pip install -r requirements.txt
```

## Data
  - The USGS 3D Elevation Program (3DEP) provides access to lidar point cloud data from the 3DEP repository. The adoption of cloud storage and computing by 3DEP allows users to work with massive datasets of lidar point cloud data without having to download them to local machines.
  - The point cloud data is freely accessible from AWS in EPT format. Entwine Point Tile (EPT) is a simple and flexible octree-based storage format for point cloud data. The organization of an EPT dataset contains JSON metadata portions as well as binary point data. The JSON file is core metadata required to interpret the contents of an EPT dataset.

## Notebooks
  - 

## Scripts
  - `file_handler`: Helper class for reading and writing different file formats
  - `get_metadata`: Creates a metadata describing boundary coordinates for all regions. This enables the package to retrieve the lidar dataset from the AWS without specifying the region by simply using the boundary value.
  - `get_data`: helper class for retrieving lidar data from AWS

## Test
