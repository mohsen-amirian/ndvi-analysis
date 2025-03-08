import pandas as pd
import os

# 📂 Define file paths (UPDATE THIS)
input_csv = "dwd\\preprocess\\data-clipped-to-de-states\\merged_precipitation.csv"  # Path to your full precipitation CSV
output_folder = "dwd\\preprocess\\final-data"  # Folder where yearly CSVs will be saved

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# 📌 Load the full precipitation dataset
df = pd.read_csv(input_csv, parse_dates=["time"])  # Ensure "time" column is parsed as dates

# 📅 Extract Year
df["Year"] = df["time"].dt.year

# 📊 Compute Mean Precipitation per State & Year
grouped_df = df.groupby(["Year", "state"])["precip"].mean().reset_index()

# Rename columns for clarity
grouped_df.rename(columns={"precip": "mean_precip"}, inplace=True)

# 🔄 Save Separate CSVs per Year
for year, year_df in grouped_df.groupby("Year"):
    output_file = os.path.join(output_folder, f"precipitation_{year}.csv")
    year_df.drop(columns=["Year"]).to_csv(output_file, index=False)
    print(f"✅ Saved: {output_file}")

print("\n✅ All yearly precipitation files are generated!")
