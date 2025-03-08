import geopandas as gpd
import xarray as xr
import pandas as pd
import geopandas as gpd
import pandas as pd
import rioxarray

# Load German states shapefile
germany_states = gpd.read_file("germany-states\\de.shp")

# Load NetCDF file
nc_file = "dwd\\40-years-prep\\full_data_monthly_v2022_1981_1990_025.nc"  # Update with the correct path
ds = xr.open_dataset(nc_file)

# Ensure NetCDF has CRS set (if missing)
if ds.rio.crs is None:
    ds.rio.write_crs("EPSG:4326", inplace=True)

# Extract the precipitation variable (without manually slicing lat/lon)
precip = ds["precip"]

# Initialize an empty list to store state-wise precipitation data
state_precip_data = []

# Loop through each German state & extract precipitation
for _, state in germany_states.iterrows():
    state_id = state["id"]  # Use state abbreviation (e.g., "DEBY", "DESN")
    state_geom = state.geometry

    # Use `rioxarray` to clip precipitation data to the state's boundary
    state_precip = precip.rio.clip([state_geom], germany_states.crs, drop=True)

    # Convert clipped xarray dataset to Pandas DataFrame & add state column
    df_state = state_precip.to_dataframe().reset_index()
    df_state["state"] = state_id

    # Store results
    state_precip_data.append(df_state)

# Merge all states' precipitation data
df_precip_by_state = pd.concat(state_precip_data)

# Save the extracted data for further analysis
df_precip_by_state.to_csv("precipitation_per_state.csv", index=False)

print("✅ Precipitation data extracted for all states and saved as '1981_1990.csv'.")