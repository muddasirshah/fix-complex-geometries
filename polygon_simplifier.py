#This script simplifies the polygons in a shapefile with greater than 500 vertices using Ramer-Douglas-Peucker algorithm while retaining the rest
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, LineString
from shapely.ops import split
from tqdm import tqdm  
import os

def simplify_geometry(geom, simplify_tolerance):
    """Simplifies geometry to reduce vertex count while preserving shape."""
    return geom.simplify(simplify_tolerance, preserve_topology=True)

def split_polygon(geom):
    """Splits a polygon into two halves along the X-axis (vertically) using a LineString."""
    minx, miny, maxx, maxy = geom.bounds
    midx = (minx + maxx) / 2
    splitter_line = LineString([(midx, miny), (midx, maxy)])
    split_geoms = split(geom, splitter_line)
    return list(split_geoms) if isinstance(split_geoms, (MultiPolygon, list)) else [split_geoms]

def process_geometry(geom, vertex_limit, simplify_tolerance):
    """Simplifies or splits the geometry based on vertex count."""
    if isinstance(geom, Polygon):
        if len(geom.exterior.coords) >= vertex_limit:
            split_geoms = split_polygon(geom)
            valid_geoms = [g for g in split_geoms if isinstance(g, Polygon) and not g.is_empty]
            if len(valid_geoms) > 1:
                return valid_geoms
            else:
                return [simplify_geometry(geom, simplify_tolerance)]
        else:
            return [geom]
    elif isinstance(geom, MultiPolygon):
        processed_polys = []
        for poly in geom:
            processed_polys.extend(process_geometry(poly, vertex_limit, simplify_tolerance))
        return processed_polys
    return [geom]

def simplify_shapefile(input_shapefile, output_shapefile, vertex_limit=500, simplify_tolerance=0.0001):
    """Loads the shapefile, simplifies or splits polygons, and saves to a new shapefile."""
    gdf = gpd.read_file(input_shapefile)
    simplified_geometries = []
    for idx, row in tqdm(gdf.iterrows(), total=gdf.shape[0], desc="Processing geometries"):
        geom = row.geometry
        processed_geometries = process_geometry(geom, vertex_limit, simplify_tolerance)
        for processed_geom in processed_geometries:
            new_row = row.copy()
            new_row.geometry = processed_geom
            simplified_geometries.append(new_row)

    new_gdf = gpd.GeoDataFrame(simplified_geometries, columns=gdf.columns)
    new_gdf.crs = gdf.crs
    new_gdf.to_file(output_shapefile, driver='ESRI Shapefile')

if __name__ == "__main__":
    input_shapefile = "input.shp"  # Replace with your input file
    output_shapefile = "output_simplified.shp"  # Replace with your output file

    simplify_shapefile(input_shapefile, output_shapefile, vertex_limit=600, simplify_tolerance=0.0001) #by default it will simplify polygons with >= 500 polygons but you can define vertex limit here and simplify tolerance as well. 
