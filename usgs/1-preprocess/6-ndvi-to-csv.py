import os
import glob
import rasterio
import geopandas as gpd
from rasterstats import zonal_stats

def extract_ndvi_by_region(ndvi_path, shapefile_path, output_csv):
    """
    Extracts the mean NDVI for each administrative region and saves it to a CSV.

    Parameters:
    - ndvi_path: Path to the NDVI raster file (.tif)
    - shapefile_path: Path to the pre-reprojected administrative regions shapefile
    - output_csv: Path to save the NDVI statistics as a CSV file
    """

    try:
        # Load the pre-reprojected shapefile
        regions = gpd.read_file(shapefile_path)

        # Open NDVI raster
        with rasterio.open(ndvi_path) as ndvi:
            ndvi_crs = ndvi.crs  # Get CRS of the raster
            ndvi_nodata = ndvi.nodata  # Get NoData value

        # ✅ Ensure the shapefile is already in the correct CRS (EPSG:32633)
        if regions.crs != ndvi_crs:
            print(f"⚠️ Shapefile CRS ({regions.crs}) does not match NDVI CRS ({ndvi_crs})")
            return

        # Compute zonal statistics (mean NDVI per region)
        stats = zonal_stats(regions, ndvi_path, stats=["mean"], nodata=ndvi_nodata, mask=True)

        # Add NDVI statistics to the GeoDataFrame
        regions["mean_ndvi"] = [s["mean"] if s["mean"] is not None else -9999 for s in stats]  # Handle missing data

        # Auto-detect region name column
        possible_columns = ["STATE_NAME", "NAME", "Region", "Admin_Name"]  # Common names
        column_name = next((col for col in possible_columns if col in regions.columns), None)

        if not column_name:
            print("⚠️ Could not find a valid region name column! Using first column as fallback.")
            column_name = regions.columns[0]

        # Save results to CSV
        regions[[column_name, "mean_ndvi"]].to_csv(output_csv, index=False)

        print(f"✅ NDVI statistics saved: {output_csv}")

    except Exception as e:
        print(f"❌ Error processing {ndvi_path}: {e}")



def batch_extract_ndvi(base_folder, shapefile_path, output_folder, start_year, end_year):
    """
    Loops through yearly folders and extracts NDVI for available seasonal files.

    Parameters:
    - base_folder: Path containing year-named folders (e.g., "2000", "2001")
    - shapefile_path: Path to the pre-reprojected Germany shapefile
    - output_folder: Folder where CSV files will be saved
    - start_year: Start of the year range (e.g., 2000)
    - end_year: End of the year range (e.g., 2010)
    """

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop through the given range of years
    for year in range(start_year, end_year + 1):
        year_folder = os.path.join(base_folder, str(year))  # Folder for that year

        # Check if year folder exists
        if not os.path.exists(year_folder):
            print(f"⚠️ Skipping {year_folder} (does not exist)")
            continue

        print(f"📅 Processing year: {year}")

        # Look for all seasonal NDVI files in the year folder
        ndvi_files = glob.glob(os.path.join(year_folder, f"{year}_*_NDVI.tif"))

        if not ndvi_files:
            print(f"⚠️ No NDVI files found for {year}")
            continue

        # Process each available NDVI file
        for ndvi_file in ndvi_files:
            season = os.path.basename(ndvi_file).split("_")[1]  # Extract season name
            output_csv = os.path.join(output_folder, f"{year}_{season}_NDVI.csv")

            print(f"➡️ Processing {ndvi_file} -> {output_csv}")

            # Run extraction function
            extract_ndvi_by_region(ndvi_file, shapefile_path, output_csv)

    print("✅ Batch processing completed!")


# Example usage:
batch_extract_ndvi(
    base_folder="C:\\Mohsen\\Thesis\\coding\\ndvi-usgs",  # Folder containing year-named subfolders
    shapefile_path="germany-states/de_reprojected.shp",  # The new reprojected shapefile
    output_folder="C:\\Mohsen\\Thesis\\coding\\csv",  # Where CSVs will be saved
    start_year=2003,
    end_year=2015
)
