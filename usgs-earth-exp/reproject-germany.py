import geopandas as gpd

def reproject_shapefile(input_shapefile, output_shapefile, target_crs="EPSG:32633"):
    """
    Reprojects a shapefile to the specified CRS and saves it.
    
    Parameters:
    - input_shapefile: Path to the input shapefile (.shp or .geojson)
    - output_shapefile: Path to save the reprojected shapefile
    - target_crs: The target CRS (default: EPSG:32633)
    """
    # Load the shapefile
    gdf = gpd.read_file(input_shapefile)
    
    # Check current CRS and reproject if necessary
    if gdf.crs != target_crs:
        print(f"Reprojecting shapefile from {gdf.crs} to {target_crs}...")
        gdf = gdf.to_crs(target_crs)
    else:
        print(f"Shapefile is already in {target_crs}, skipping reprojection.")
    
    # Save the reprojected shapefile
    gdf.to_file(output_shapefile)
    print(f"✅ Reprojected shapefile saved to {output_shapefile}")

# Example usage
reproject_shapefile("germany-states/de.shp", "germany-states/de_reprojected.shp")
