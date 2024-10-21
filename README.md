# Vector Processing Tools

## Overview
This repository contains two Python scripts designed for processing shapefiles:

1. **Polygon Splitter**: This script splits polygons with a vertex count greater than or equal to 500 while retaining their properties in the output file.
2. **Polygon Simplifier**: This script simplifies geometries in a shapefile by reducing the vertex count of polygons while preserving their shape.

Both scripts leverage the powerful `geopandas` library, along with `shapely` for geometric operations and `tqdm` for progress visualization.

## Requirements
To run these scripts, you need an Anaconda or Miniconda environment with the following dependencies:

- Python 3.9
- GDAL
- Shapely
- TQDM
- GeoPandas

### Installation Steps
1. **Install Anaconda/Miniconda**:
   If you haven't installed Anaconda or Miniconda, download and install it from the [official website](https://www.anaconda.com/products/distribution#download-section).

2. **Create a New Conda Environment**:
   Open a terminal or Anaconda Prompt and create a new conda environment:
   ```bash
   conda create -n geospatial_tools python=3.9 gdal geopandas shapely tqdm
3. **Activate the Conda Environment**:
   ```bash
   conda activate geospatial_tools

### Notes:
- You can customize this template further based on your project's specific details or additional instructions you might want to include.

Let me know if you need any further modifications or additional sections!



