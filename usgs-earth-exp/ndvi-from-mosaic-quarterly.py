import os
import numpy as np
import rasterio

def compute_ndvi(red_band_path, nir_band_path, output_ndvi_path):
    """
    Computes NDVI from Red and NIR band mosaics and saves the output as a GeoTIFF.
    """
    print(f'Processing {red_band_path} and {nir_band_path}...')
    try:
        with rasterio.open(red_band_path) as red, rasterio.open(nir_band_path) as nir:
            B_red = red.read(1).astype(np.float32)
            B_nir = nir.read(1).astype(np.float32)

            np.seterr(divide='ignore', invalid='ignore')
            ndvi = (B_nir - B_red) / (B_nir + B_red)
            ndvi[np.isnan(ndvi)] = -9999

            out_meta = red.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "dtype": "float32",
                "compress": "LZW",
                "nodata": -9999
            })

            with rasterio.open(output_ndvi_path, "w", **out_meta) as dst:
                dst.write(ndvi, 1)

        print(f"✅ NDVI saved successfully: {output_ndvi_path}")
    except Exception as e:
        print(f"⚠️ Error processing {red_band_path} and {nir_band_path}: {e}")

def process_ndvi_for_years(start_year, end_year, base_dir, output_dir):
    """
    Processes NDVI for a range of years, handling different Landsat versions.
    """
    landsat_bands = {
        "pre_2014": {"red": "B3", "nir": "B4"},
        "post_2014": {"red": "B4", "nir": "B5"}
    }
    
    for year in range(start_year, end_year + 1):
        print(f'{year} Prosessing ..!')
        year_folder = os.path.join(base_dir, str(year))
        
        landsat_version = "pre_2014" if year < 2014 else "post_2014"
        red_band_suffix = landsat_bands[landsat_version]["red"]
        nir_band_suffix = landsat_bands[landsat_version]["nir"]

        seasons = ["Winter", "Spring", "Summer", "Fall"]
        available_files = os.listdir(year_folder)
        
        for season in seasons:
            red_band = next((f for f in available_files if season in f and red_band_suffix in f), None)
            nir_band = next((f for f in available_files if season in f and nir_band_suffix in f), None)

            if not red_band or not nir_band:
                print(f"⚠️ Missing bands for {season} {year}, skipping...")
                continue
            
            red_band_path = os.path.join(year_folder, red_band)
            nir_band_path = os.path.join(year_folder, nir_band)
            output_ndvi_path = os.path.join(output_dir, f"{year}_{season}_NDVI.tif")

            compute_ndvi(red_band_path, nir_band_path, output_ndvi_path)
            print(f'{year} - {season} Done!')
        print(f'{year} Finished!')
        print('-------------------------------------------------------------')
        print('-------------------------------------------------------------')

# Example usage
base_directory = "C:\\Mohsen\\Thesis\\coding\\mosaic-usgs"  # Update with actual path
output_directory = "C:\\Mohsen\\Thesis\\coding\\ndvi-usgs"  # Update with actual path
os.makedirs(output_directory, exist_ok=True)

process_ndvi_for_years(2007, 2007, base_directory, output_directory)
