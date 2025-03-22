import os
import glob
import rasterio
import geopandas as gpd
import pandas as pd
import numpy as np
from rasterio.mask import mask
from shapely.geometry import mapping

# Folder paths (UPDATE THESE)
raster_folder = "dwd-sunshine\\data\\0-extracted\\"  # Change to your folder containing .asc files
geojson_path = "germany-states\\germany-states.geojson"  # Change to your GeoJSON file
output_folder = "dwd-sunshine\\data\\output_csv"  # Change to your output folder

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load the GeoJSON file (Germany states)
germany_states = gpd.read_file(geojson_path)

# Get all .asc files in the folder
asc_files = glob.glob(os.path.join(raster_folder, "grids_germany_annual_sunshine_duration_*.asc"))

# Loop through each ASC file and process
for raster_path in asc_files:
    # Extract the year from the filename
    filename = os.path.basename(raster_path)  # Get file name
    year = filename.split("_")[-1][:4]  # Extract 1985, 1986, ..., 2024

    print(f"Processing: {filename} (Year: {year})")

    # Open the raster file
    with rasterio.open(raster_path) as src:
        raster_crs = src.crs  # Get the CRS of the raster

        # If the raster has no CRS, manually assign EPSG:31467
        if raster_crs is None:
            raster_crs = "EPSG:31467"

        # Reproject GeoJSON to match raster CRS if necessary
        if germany_states.crs != raster_crs:
            germany_states = germany_states.to_crs(raster_crs)

        # Prepare a list to store results
        temperature_data = []

        # Loop through each state and extract temperature data
        for index, row in germany_states.iterrows():
            state_name = row["NAME_1"]  # Update if needed

            # Convert state geometry to raster's CRS
            geojson_geom = [mapping(row.geometry)]

            # Clip the raster to the state boundary
            out_image, out_transform = mask(src, geojson_geom, crop=True)

            # Extract valid temperature values (ignoring nodata values)
            temp_values = out_image[0].flatten()
            temp_values = temp_values[temp_values != src.nodata]  # Remove NoData values

            # Convert temperature from tenths of degrees Celsius if needed
            temp_values = temp_values / 10.0  # Assuming values are stored in tenths of °C

            # Calculate statistics
            mean_temp = np.nanmean(temp_values) if temp_values.size > 0 else None

            # Append to results
            temperature_data.append({
                "State": state_name,
                "Mean_Sunshine": mean_temp
            })

    # Convert results to DataFrame and save as CSV
    df = pd.DataFrame(temperature_data)
    output_csv_path = os.path.join(output_folder, f"sunshine_{year}.csv")
    df.to_csv(output_csv_path, index=False)

    print(f"Saved: {output_csv_path}")

print("\n✅ All files processed successfully!")
