import rasterio
import numpy as np
import matplotlib.pyplot as plt

def plot_ndvi(ndvi_path):
    """
    Plots the NDVI raster with a color scale.

    Parameters:
    - ndvi_path: Path to the NDVI raster file.
    """

    # Open NDVI raster
    with rasterio.open(ndvi_path) as src:
        ndvi = src.read(1)  # Read the first band

    # Mask no-data values (-9999)
    ndvi = np.ma.masked_where(ndvi == -9999, ndvi)

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)  # Use vegetation colormap
    plt.colorbar(label="NDVI Value")  # Add color scale
    plt.title("NDVI Visualization")
    plt.xlabel("Pixel X")
    plt.ylabel("Pixel Y")
    plt.show()

# Example usage
plot_ndvi("NDVI_Spring_2024.tif")

# we can have plots next to each other for comparison
