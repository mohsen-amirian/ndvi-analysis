import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 📂 Define paths (UPDATE THESE)
ndvi_folder = "usgs\\0-data\\1-final-ndvi-per-year"
sunshine_folder = "dwd-sunshine\\data\\2-final-data-state-code"
output_file = "full-analyze\\data\\merged_ndvi_sunshine.csv"

# Get all NDVI & Sunshine CSV files
ndvi_files = sorted([f for f in os.listdir(ndvi_folder) if f.startswith("ndvi_") and f.endswith(".csv")])
sunshine_files = sorted([f for f in os.listdir(sunshine_folder) if f.startswith("sunshine_") and f.endswith(".csv")])

# 🔄 Merge Data
merged_data = []

for ndvi_file, sunshine_file in zip(ndvi_files, sunshine_files):
    year = ndvi_file.split("_")[-1].split(".")[0]  # Extract year
    
    # Load CSV files
    ndvi_df = pd.read_csv(os.path.join(ndvi_folder, ndvi_file))
    sunshine_df = pd.read_csv(os.path.join(sunshine_folder, sunshine_file))

    # Rename columns for consistency
    ndvi_df.rename(columns={"state": "State"}, inplace=True)

    # Merge on "State"
    merged_df = pd.merge(ndvi_df, sunshine_df[["State", "Mean_Sunshine"]], on="State", how="inner")

    # Add Year Column
    merged_df["Year"] = int(year)

    # Append data
    merged_data.append(merged_df)

# Combine all years
final_df = pd.concat(merged_data, ignore_index=True)

# Save merged data
final_df.to_csv(output_file, index=False)
print(f"✅ Merged data saved as: {output_file}")
