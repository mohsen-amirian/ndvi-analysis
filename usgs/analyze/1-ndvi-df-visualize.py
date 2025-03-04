import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# Load NDVI data from a CSV file
ndvi_df = pd.read_csv("usgs\\analyze\\data\\ndvi_full_df.csv")

# 🔹 Visualization 🔹

# 🎯 A. Line Plot: NDVI Trend Over Time (Grouped by State)
# plt.figure(figsize=(12, 6))
# sns.lineplot(data=ndvi_df, x="year", y="mean_ndvi", hue="state_name", marker="o", alpha=0.7)
# plt.title("NDVI Trends Over Time by State")
# plt.xlabel("Year")
# plt.ylabel("Mean NDVI")
# plt.legend(title="State", bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.grid()
# plt.show()

# 🎯 B. Boxplot: NDVI Variability Across States
# plt.figure(figsize=(12, 6))
# sns.boxplot(data=ndvi_df, x="state_name", y="mean_ndvi")
# plt.title("NDVI Variability Across German States")
# plt.xlabel("State")
# plt.ylabel("Mean NDVI")
# plt.xticks(rotation=90)
# plt.grid()
# plt.show()

# 🎯 C. Heatmap: NDVI Trends by State Over Years
pivot_table = ndvi_df.pivot_table(values="mean_ndvi", index="state_name", columns="year", aggfunc="mean")

# Ensure data is numeric before plotting the heatmap
pivot_table = pivot_table.astype(float)

plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, cmap="coolwarm", linewidths=0.5)
plt.title("NDVI Trends by State Over Time")
plt.xlabel("Year")
plt.ylabel("State")
plt.show()
