import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import os
import utils.filesUtil as f
import shutil


def reproject_raster(input_path, output_path, index, target_crs="EPSG:32633"):
    with rasterio.open(input_path) as src:
        # Check if the source CRS is already the target CRS
        if src.crs.to_string() == target_crs:
            print(f"{index} - Input raster is already in target CRS. Copying file.")
            shutil.copy(input_path, output_path)
            return
        else:
            print(f"{index} - Projecting file from {src.crs.to_string()} to {target_crs}.")

        # Compute transformation for the new CRS
        transform, width, height = calculate_default_transform(
            src.crs, target_crs, src.width, src.height, *src.bounds
        )

        kwargs = src.meta.copy()
        kwargs.update({
            'crs': target_crs,
            'transform': transform,
            'width': width,
            'height': height
        })

        with rasterio.open(output_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=target_crs,
                    resampling=Resampling.nearest  # Use nearest-neighbor interpolation
                )


for year in range(2014, 2017):  
    files_to_reproject = f.list_files_in_folder(f'C:\\Users\\M0H3N\\Downloads\\USGS\\{year}')
    
    index = 1
    for file in files_to_reproject:
        output_folder = f"C:\\Users\\M0H3N\\Downloads\\USGS\\R\\{year}R"
        os.makedirs(output_folder, exist_ok=True)  # Create folder if it doesn’t exist
        output_file = os.path.join(output_folder, os.path.basename(file))
        reproject_raster(file, output_file, index, "EPSG:32633")  # Convert everything to EPSG:32633
        index += 1

print('Finished')