import os
import rasterio
import shutil
from rasterio.merge import merge
from datetime import datetime

def create_mosaic(input_files, output_filename):
    """
    Creates a mosaic from input raster files and saves it.
    """
    if not input_files:
        print(f"No files found for {output_filename}")
        return
    
    src_files_to_mosaic = [rasterio.open(f) for f in input_files]
    mosaic, out_trans = merge(src_files_to_mosaic)
    mosaic = mosaic.astype("float32") / 10000.0  # Normalize values
    
    out_meta = src_files_to_mosaic[0].meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "height": mosaic.shape[1],
        "width": mosaic.shape[2],
        "transform": out_trans,
        "dtype": "float32",
        "compress": "LZW"
    })
    
    with rasterio.open(output_filename, "w", **out_meta) as dest:
        dest.write(mosaic.astype("float32"))
    
    for src in src_files_to_mosaic:
        src.close()

def process_yearly_data(start_year, end_year, base_path, output_path):
    """
    Processes raster data in a given year range, creating mosaics per season.
    """
    season_labels = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
    
    for year in range(start_year, end_year + 1):
        year_folder = os.path.join(base_path, f"{year}RT")
        
        b5_files, b4_files = {1: [], 2: [], 3: [], 4: []}, {1: [], 2: [], 3: [], 4: []}
        
        for filename in os.listdir(year_folder):
            if filename.endswith(".TIF"):
                parts = filename.split("_")
                date_str = parts[3]  # Extract date from filename
                date_obj = datetime.strptime(date_str, "%Y%m%d")
                quarter = (date_obj.month - 1) // 3 + 1  # Calculate quarter
                file_path = os.path.join(year_folder, filename)
                
                if "_SR_B5" in filename:
                    b5_files[quarter].append(file_path)
                elif "_SR_B4" in filename:
                    b4_files[quarter].append(file_path)
        
        for quarter in range(1, 5):
            season = season_labels[quarter]
            output_b5 = os.path.join(output_path, f"{year}_{season}_B5.tif")
            output_b4 = os.path.join(output_path, f"{year}_{season}_B4.tif")
            create_mosaic(b5_files[quarter], output_b5)
            create_mosaic(b4_files[quarter], output_b4)
        
        # Remove original folder after processing
        shutil.rmtree(year_folder, ignore_errors=True)
        print(f"Deleted folder: {year_folder}")

# Example usage
process_yearly_data(2014, 2015, "C:\\Users\\M0H3N\\Downloads\\USGS", "C:\\Users\\M0H3N\\Downloads\\USGS-Mosaics")
