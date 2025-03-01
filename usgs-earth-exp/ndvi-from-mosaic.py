import rasterio
import numpy as np

def compute_ndvi(red_band_path, nir_band_path, output_ndvi_path):
    """
    Computes NDVI from Red (B4) and NIR (B5) band mosaics and saves the output as a GeoTIFF.

    Parameters:
    - red_band_path: Path to the Red band (B4) mosaic.
    - nir_band_path: Path to the NIR band (B5) mosaic.
    - output_ndvi_path: Path to save the computed NDVI raster.
    """

    # Open the Red (B4) and NIR (B5) mosaics
    with rasterio.open(red_band_path) as red, rasterio.open(nir_band_path) as nir:
        B4 = red.read(1).astype(np.float32)  # Read Red band
        B5 = nir.read(1).astype(np.float32)  # Read NIR band

        # Ensure no division by zero: NDVI = (NIR - Red) / (NIR + Red)
        np.seterr(divide='ignore', invalid='ignore')  # Ignore division warnings
        ndvi = (B5 - B4) / (B5 + B4)

        # Handle NaNs and set nodata value (-9999 for consistency)
        ndvi[np.isnan(ndvi)] = -9999

        # Get metadata from the original image
        out_meta = red.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "dtype": "float32",  # NDVI values are float
            "compress": "LZW"    # Lossless compression
        })

        # Save NDVI raster
        with rasterio.open(output_ndvi_path, "w", **out_meta) as dst:
            dst.write(ndvi, 1)  # Write NDVI data as band 1

    print(f"✅ NDVI saved successfully: {output_ndvi_path}")

# Example usage
compute_ndvi("Mosaic_2024_Spring_B4.tif", "Mosaic_2024_Spring_B5.tif", "NDVI_Spring_2024.tif")
