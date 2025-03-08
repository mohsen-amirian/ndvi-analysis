import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load NDVI Data
df_1999 = pd.read_csv("usgs\\0-data\\1-final-ndvi-per-year\\ndvi_1999.csv")

# Histogram to Check Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df_1999["mean_ndvi"], bins=10, kde=True)
plt.title("NDVI Distribution - 1999 (Germany)")
plt.xlabel("Mean NDVI")
plt.ylabel("Frequency")
plt.show()
