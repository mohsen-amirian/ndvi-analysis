import rasterio
import geopandas as gpd
import pandas as pd
from rasterstats import zonal_stats

def extract_ndvi_by_region(ndvi_path, shapefile_path, output_csv):
    """
    Extracts the mean NDVI for each administrative region in Germany and saves it to a CSV.

    Parameters:
    - ndvi_path: Path to the NDVI raster file (.tif)
    - shapefile_path: Path to the administrative regions shapefile (.shp or .geojson)
    - output_csv: Path to save the NDVI statistics as a CSV file
    """

    # Load the shapefile
    regions = gpd.read_file(shapefile_path)

    # Open NDVI raster and get its CRS
    with rasterio.open(ndvi_path) as ndvi:
        target_crs = ndvi.crs  # CRS of the NDVI raster

    # ✅ Reproject the shapefile to match NDVI CRS if needed
    if regions.crs != target_crs:
        print(f"⚠️ Reprojecting shapefile from {regions.crs} to {target_crs}...")
        regions = regions.to_crs(target_crs)

    # Compute zonal statistics (mean NDVI per region)
    stats = zonal_stats(regions, ndvi_path, stats=["mean"], nodata=-9999, mask=True)

    # Add NDVI statistics to the GeoDataFrame
    regions["mean_ndvi"] = [s["mean"] for s in stats]

    # Check column name for region names
    print("Shapefile Columns:", regions.columns)  # Check available columns

    # Replace "STATE_NAME" with the actual column containing region names
    column_name = "STATE_NAME" if "STATE_NAME" in regions.columns else regions.columns[0]  # Auto-detect column

    # Save results to CSV
    regions[[column_name, "mean_ndvi"]].to_csv(output_csv, index=False)

    print(f"✅ NDVI statistics saved successfully: {output_csv}")

# Example usage
extract_ndvi_by_region("NDVI_Spring_2024.tif", "germany-states/de.shp", "NDVI_by_region_2024.csv")