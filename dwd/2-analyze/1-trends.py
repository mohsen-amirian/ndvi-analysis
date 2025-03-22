import pandas as pd
import matplotlib.pyplot as plt

# Load the precipitation dataset
file_path = "dwd\\0-data\\1-data-clipped-to-de-states\\merged_precipitation.csv"
precip_df = pd.read_csv(file_path)

# Convert time column to datetime format
precip_df["time"] = pd.to_datetime(precip_df["time"])

# Extract year from the date
precip_df["year"] = precip_df["time"].dt.year

# Compute mean annual precipitation across all states
annual_precip_trend = precip_df.groupby("year")["precip"].mean()

# Plot precipitation trend over time
plt.figure(figsize=(10, 5))
plt.plot(annual_precip_trend.index, annual_precip_trend.values, marker='o', linestyle='-', linewidth=2, color='b')
plt.xlabel("Year")
plt.ylabel("Mean Precipitation (mm)")
plt.title("Annual Precipitation Trend in Germany (1985–2020)")
plt.grid(True)

# Show plot
plt.show()
