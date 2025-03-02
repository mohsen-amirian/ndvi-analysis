import rasterio
import numpy as np

def compute_ndvi(red_band_path, nir_band_path, output_ndvi_path):
    """
    Computes NDVI from Red (B3) and NIR (B4) band mosaics for Landsat 5 and saves the output as a GeoTIFF.

    Parameters:
    - red_band_path: Path to the Red band (B3) mosaic.
    - nir_band_path: Path to the NIR band (B4) mosaic.
    - output_ndvi_path: Path to save the computed NDVI raster.
    """
    print('Started ..')
    # Open the Red (B3) and NIR (B4) mosaics
    with rasterio.open(red_band_path) as red, rasterio.open(nir_band_path) as nir:
        B3 = red.read(1).astype(np.float32)  # Red Band (B3)
        B4 = nir.read(1).astype(np.float32)  # NIR Band (B4)

        # Ensure no division by zero: NDVI = (NIR - Red) / (NIR + Red)
        np.seterr(divide='ignore', invalid='ignore')  # Ignore division warnings
        ndvi = (B4 - B3) / (B4 + B3)

        # Handle NaNs and set nodata value (-9999 for consistency)
        ndvi[np.isnan(ndvi)] = -9999

        # Get metadata from the original image
        out_meta = red.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "dtype": "float32",  # NDVI values are float
            "compress": "LZW",    # Lossless compression
            "nodata": -9999       # Set nodata value
        })

        # Save NDVI raster
        with rasterio.open(output_ndvi_path, "w", **out_meta) as dst:
            dst.write(ndvi, 1)  # Write NDVI data as band 1

    print(f"✅ NDVI saved successfully: {output_ndvi_path}")

#L5 and L7
# red B3 
# NIR B4 

#L8
# red B4 
# NIR B5 

# Example usage
compute_ndvi("C:\\Mohsen\\temp-usgs\\_mosaics\\1986_Fall_B3.tif", "C:\\Mohsen\\temp-usgs\\_mosaics\\1986_Fall_B4.tif", "1986_Fall_NDVI.tif")
