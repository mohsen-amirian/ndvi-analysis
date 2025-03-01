import rasterio

with rasterio.open("Mosaic_2024_05_B5.tif") as src:
    print("Data Type:", src.dtypes[0])  # Should be float32 or int16
    print("Compression:", src.profile.get("compress", "None"))