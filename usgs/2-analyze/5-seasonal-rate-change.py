import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Load the NDVI dataset
file_path = "usgs\\0-data\\ndvi_full_df.csv"  # Update with your actual file path
ndvi_df = pd.read_csv(file_path)

# Compute NDVI trend slopes per season using linear regression
season_trends = {}

for season in ndvi_df["season"].unique():
    season_data = ndvi_df[ndvi_df["season"] == season].groupby("year")["mean_ndvi"].mean()
    slope, intercept, r_value, p_value, std_err = stats.linregress(season_data.index, season_data.values)
    season_trends[season] = slope

# Convert to DataFrame for visualization
df_season_trends = pd.DataFrame.from_dict(season_trends, orient='index', columns=["NDVI Trend Slope"])

# Create a bar chart to visualize NDVI rate of change per season
plt.figure(figsize=(8, 5))
df_season_trends["NDVI Trend Slope"].plot(kind="bar", color=["blue", "orange", "green", "red"])
plt.xlabel("Season")
plt.ylabel("NDVI Trend Slope")
plt.title("NDVI Rate of Change Per Season (1985–2024)")
plt.grid(axis="y")

# Show plot
plt.show()
