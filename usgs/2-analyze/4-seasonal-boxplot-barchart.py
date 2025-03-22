import pandas as pd
import matplotlib.pyplot as plt

# Load the NDVI dataset
file_path = "usgs\\0-data\\ndvi_full_df.csv" 
ndvi_df = pd.read_csv(file_path)

# Create a boxplot to compare NDVI distributions across seasons
plt.figure(figsize=(10, 6))
ndvi_df.boxplot(column="mean_ndvi", by="season", grid=False, showfliers=False)
plt.xlabel("Season")
plt.ylabel("Mean NDVI")
plt.title("NDVI Comparison Across Seasons (1985–2024)")
plt.suptitle("")  # Remove automatic boxplot title
plt.show()

# Compute the mean NDVI for each season
seasonal_means = ndvi_df.groupby("season")["mean_ndvi"].mean()

# Create a bar chart to compare mean NDVI across seasons
plt.figure(figsize=(8, 5))
seasonal_means.plot(kind="bar", color=["blue", "orange", "green", "red"])
plt.xlabel("Season")
plt.ylabel("Mean NDVI")
plt.title("Average NDVI Per Season (1985–2024)")
plt.grid(axis="y")
plt.show()
