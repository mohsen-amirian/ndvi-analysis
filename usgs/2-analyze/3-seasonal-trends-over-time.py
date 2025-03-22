import pandas as pd
import matplotlib.pyplot as plt

# Load the NDVI dataset
file_path = "usgs\\0-data\\ndvi_full_df.csv" 
ndvi_df = pd.read_csv(file_path)

# Compute mean NDVI per season for each year
seasonal_ndvi_trend = ndvi_df.groupby(["year", "season"])["mean_ndvi"].mean().unstack()

# Plot NDVI trends for each season
plt.figure(figsize=(12, 6))

for season in seasonal_ndvi_trend.columns:
    plt.plot(seasonal_ndvi_trend.index, seasonal_ndvi_trend[season], marker='o', linestyle='-', label=season)

plt.xlabel("Year")
plt.ylabel("Mean NDVI")
plt.title("Seasonal NDVI Trends Over Time (1985–2024)")
plt.legend(title="Season")
plt.grid(True)

# Show plot
plt.show()
