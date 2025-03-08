import pandas as pd
import glob

folder_name = 'dwd\\preprocess\\data-clipped-to-de-states'

# List all cleaned CSV files
csv_files = [
    f"{folder_name}\\1981_1990-cleaned.csv",
    f"{folder_name}\\1991_2000-cleaned.csv",
    f"{folder_name}\\2001_2010-cleaned.csv",
    f"{folder_name}\\2011_2020-cleaned.csv"
]

# Read and concatenate all CSV files
df_precip_all = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)

# Save the merged dataset
df_precip_all.to_csv(f"{folder_name}\\merged_precipitation.csv", index=False)

print("✅ All precipitation data merged and saved as 'merged_precipitation.csv'.")
