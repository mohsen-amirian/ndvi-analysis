import pandas as pd

file_name = '2011_2020'

# Load the extracted precipitation data
df_precip = pd.read_csv(f"dwd\\preprocess\\data-clipped-to-de-states\\{file_name}.csv")

# Drop the spatial_ref column (not needed)
df_precip.drop(columns=["spatial_ref"], inplace=True)

# Remove rows where 'precip' is missing (NaN)
df_precip = df_precip.dropna(subset=["precip"])

# Save the cleaned dataset
df_precip.to_csv(f"dwd\\preprocess\\data-clipped-to-de-states\\{file_name}-cleaned.csv", index=False)

print("✅ Cleaned precipitation data saved as 'cleaned_precipitation_per_state.csv'.")
