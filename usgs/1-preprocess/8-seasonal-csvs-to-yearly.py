import os
import pandas as pd

# 📂 Define input & output folder paths 
input_csv = "usgs\\0-data\\ndvi_full_df.csv"  # Path to the NDVI dataset
output_folder = "usgs\\0-data\\1-ndvi-per-year"  # Folder for processed NDVI CSVs

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# 📌 Load the NDVI dataset
df = pd.read_csv(input_csv)

# 📌 Drop rows where "mean_ndvi" is completely missing
df = df.dropna(subset=["mean_ndvi"])

# 📊 Step 1: Compute mean NDVI per state & season
seasonal_means = df.groupby(["year", "id", "season"])["mean_ndvi"].mean().reset_index()

# 📊 Step 2: Compute annual mean NDVI by averaging seasonal means
annual_ndvi = seasonal_means.groupby(["year", "id"])["mean_ndvi"].mean().reset_index()

# 📌 Rename columns
annual_ndvi.rename(columns={"id": "state"}, inplace=True)

# 🔄 Step 3: Save Separate CSVs per Year
for year, year_df in annual_ndvi.groupby("year"):
    output_file = os.path.join(output_folder, f"ndvi_{year}.csv")
    year_df.drop(columns=["year"]).to_csv(output_file, index=False)
    print(f"✅ Saved: {output_file}")

print("\n✅ All NDVI files processed & saved per year!")
