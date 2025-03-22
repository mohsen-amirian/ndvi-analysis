import os
import pandas as pd

# 📂 Define folder paths (UPDATE THESE)
ndvi_folder = "usgs\\0-data\\1-final-ndvi-per-year"
precip_folder = "dwd\\0-data\\2-final-data"
output_file = "full-analyze\\data\\merged_ndvi_precipitation.csv"

# 📌 Set the range of years
start_year = 1985
end_year = 2020
years = range(start_year, end_year + 1)

# 📊 List to store merged yearly data
merged_data = []

# 🔄 Process each year
for year in years:
    ndvi_file = os.path.join(ndvi_folder, f"ndvi_{year}.csv")
    precip_file = os.path.join(precip_folder, f"precipitation_{year}.csv")
    
    # Check if both files exist
    if not (os.path.exists(ndvi_file) and os.path.exists(precip_file)):
        print(f"⚠️ Skipping {year}: Missing NDVI or Precipitation file")
        continue
    
    # Load the CSV files
    ndvi_df = pd.read_csv(ndvi_file)
    precip_df = pd.read_csv(precip_file)

    # Ensure column names are consistent
    ndvi_df.rename(columns={"state": "State"}, inplace=True)
    precip_df.rename(columns={"state": "State"}, inplace=True)

    # Merge on "State"
    merged_df = pd.merge(ndvi_df, precip_df, on="State", how="inner")

    # Add Year Column
    merged_df["Year"] = year

    # Append data to the list
    merged_data.append(merged_df)

# 📌 Combine all years into a single DataFrame
final_df = pd.concat(merged_data, ignore_index=True)

# 💾 Save the final merged dataset
final_df.to_csv(output_file, index=False)

print(f"\n✅ Merged dataset saved as: {output_file}")
