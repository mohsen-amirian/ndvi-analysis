import xarray as xr
import numpy as np
import glob
import gzip
import shutil
import os
import matplotlib.pyplot as plt
import pandas as pd

# Define the bounding box for Germany
LAT_MIN, LAT_MAX = 47, 55  # Latitude range for Germany
LON_MIN, LON_MAX = 5, 15   # Longitude range for Germany

def extract_gz_file(gz_file, output_folder="unzipped_nc_files"):
    """Extracts .gz file into a specified folder."""
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, os.path.basename(gz_file).replace(".gz", ""))
    
    with gzip.open(gz_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    
    return output_file

def load_and_filter_precipitation(nc_files):
    """Loads precipitation data and filters for Germany."""
    all_data = []
    
    for nc_file in nc_files:
        ds = xr.open_dataset(nc_file)
        
        # Select precipitation variable
        precip = ds['precip']
        
        # Filter for Germany's latitude & longitude
        precip_germany = precip.sel(latitude=slice(LAT_MAX, LAT_MIN), longitude=slice(LON_MIN, LON_MAX))
        
        # Convert to DataFrame and store
        df = precip_germany.to_dataframe().reset_index()
        all_data.append(df)
        
    return all_data

def analyze_precipitation(data_frames):
    """Analyzes and visualizes precipitation trends over 40 years."""
    df_all = pd.concat(data_frames)
    df_all['time'] = pd.to_datetime(df_all['time'])
    
    # Compute yearly mean precipitation for Germany
    yearly_precip = df_all.groupby(df_all['time'].dt.year)['precip'].mean()
    
    # Plot the precipitation trend
    plt.figure(figsize=(12, 6))
    plt.plot(yearly_precip.index, yearly_precip.values, marker='o', linestyle='-', color='b')
    plt.xlabel('Year')
    plt.ylabel('Mean Precipitation (mm)')
    plt.title('Precipitation Trend in Germany (Past 40 Years)')
    plt.grid()
    plt.show()

# Step 1: Extract all .gz files
nc_files = [extract_gz_file(f) for f in glob.glob("*.nc.gz")]

# Step 2: Load & filter precipitation data for Germany
data_frames = load_and_filter_precipitation(nc_files)

# Step 3: Analyze and visualize precipitation trends
analyze_precipitation(data_frames)
