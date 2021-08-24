# PythonLidar

**Table of content**
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Install](#install)
  - [Data](#data)
  - [Notebooks](#notebooks)
  - [Scripts](#scripts)
  - [Test](#test)

## Overview
PythonLidar is an open-source python package for retrieving, transforming, and visualizing point cloud data obtained through an aerial LiDAR survey. Using the package, you can select a region of interest, and download the related point cloud dataset with its metadata in different file formats (.laz, .tif, or as an ASCII file), perform transformation and visualization using the downloaded data.

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

## How to Use

