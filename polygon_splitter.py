import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, LineString, GeometryCollection
from shapely.ops import split
from tqdm import tqdm
vertices_threshold = 500 #input the polygon vertices threshold you want to split. i.e. a polygons having more than 500 vertices will be split, rest will be retained
def split_polygon(geom):
    """Splits a polygon into two halves along the X-axis (vertically) using a LineString."""
    minx, miny, maxx, maxy = geom.bounds
    midx = (minx + maxx) / 2
    splitter_line = LineString([(midx, miny), (midx, maxy)])
    split_geoms = split(geom, splitter_line)
    if isinstance(split_geoms, (MultiPolygon, GeometryCollection)):
        return [g for g in split_geoms.geoms if isinstance(g, (Polygon, MultiPolygon)) and not g.is_empty]
    else:
        return [split_geoms] if isinstance(split_geoms, (Polygon, MultiPolygon)) and not split_geoms.is_empty else []

def process_geometry(geom, properties):
    """Splits the geometry if it has more than 10 vertices and assigns the original properties to new geometries."""
    if isinstance(geom, Polygon):
        vertex_count = len(geom.exterior.coords)
        print(f"Processing Polygon with {vertex_count} vertices.")
        if vertex_count >= vertices_threshold:
            split_geoms = split_polygon(geom)
            for g in split_geoms:
                print(f"Valid split geometry with {len(g.exterior.coords)} vertices.")
                yield (g, properties)
        else:
            yield (geom, properties)
    elif isinstance(geom, MultiPolygon):
        for poly in geom:
            yield from process_geometry(poly, properties)

def split_shapefile(input_shapefile, output_shapefile):
    """Loads the shapefile, splits polygons with more than 10 vertices, and saves the new geometries to a new shapefile."""
    gdf = gpd.read_file(input_shapefile)

    split_geometries = []
    for idx, row in tqdm(gdf.iterrows(), total=gdf.shape[0], desc="Splitting geometries"):
        geom = row.geometry
        properties = row.drop('geometry').to_dict()
        processed_geometries = list(process_geometry(geom, properties))
        split_geometries.extend(processed_geometries)

    if split_geometries:
        geometries, properties_list = zip(*split_geometries)
        properties_df = gpd.GeoDataFrame(properties_list, geometry=list(geometries))
        properties_df.crs = gdf.crs
        properties_df.to_file(output_shapefile, driver='ESRI Shapefile')
    else:
        print("No valid geometries to save.")

if __name__ == "__main__":
    input_shapefile = "input.shp"  # Replace with your input file
    output_shapefile = "output_split.shp"  # Replace with your output file

    split_shapefile(input_shapefile, output_shapefile)
