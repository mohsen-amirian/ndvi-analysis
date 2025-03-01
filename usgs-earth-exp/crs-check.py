import rasterio
import utils.filesUtil as f

def check_crs(files):
    crs_set = set()  # Use a set to store unique CRS values
    for file in files:
        with rasterio.open(file) as src:
            crs_set.add(str(src.crs))  # Convert CRS to string to ensure uniqueness

    # Print distinct CRS values
    print("Distinct CRS found:")
    for crs in crs_set:
        print(crs)

# Example Usage
year = 2013
b5_files = f.list_files_in_folder(f'C:\\Users\\M0H3N\\Downloads\\USGS\\{year}')
check_crs(b5_files)
