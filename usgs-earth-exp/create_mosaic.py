import rasterio
import numpy as np
from rasterio.merge import merge
import glob
import os

def get_files(pattern):
    data_folder = "C:\\Mohsen\\Thesis\\coding\\ee-project\\usgs-earth-exp\\reprojected_spring"
    return glob.glob(os.path.join(data_folder, pattern))

def create_mosaic(input_files, output_filename):
    # Open all files
    src_files_to_mosaic = [rasterio.open(f) for f in input_files]
    
    # Merge into one mosaic
    mosaic, out_trans = merge(src_files_to_mosaic)
    mosaic = mosaic.astype("float32") / 10000.0
    # Save the mosaic
    out_meta = src_files_to_mosaic[0].meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans,
        "dtype": "float32",  # Ensure float32 to preserve quality
        "compress": "LZW"   
    })
    
    with rasterio.open(output_filename, "w", **out_meta) as dest:
        dest.write(mosaic.astype("float32"))

# Example for B5 and B4 band
b4_files = get_files("LC08*_2024*_B4.tif")
b5_files = get_files("LC08*_2024*_B5.tif")
create_mosaic(b4_files, "Mosaic_2024_Spring_B4.tif")

# Example for Spring 2024 B5 band
#b5_spring_files = get_files("LC08*_202403*_B5.tif") + get_files("LC08*_202404*_B5.tif") + get_files("LC08*_202405*_B5.tif")
#create_mosaic(b5_spring_files, "Mosaic_2024_Spring_B5.tif")
