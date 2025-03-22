import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

merged_csv_path = "full-analyze\\data\\merged_ndvi_temperature.csv"

merged_df = pd.read_csv(merged_csv_path)

# Compute Correlation Matrix
correlation_matrix = merged_df[["Temperature", "mean_ndvi"]].corr(method="pearson")

# Plot Correlation Heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5, fmt=".2f")
plt.title("Correlation Between Temperature & NDVI")
plt.show()


###########################################################

# sns.lmplot(data=merged_df, x="Temperature", y="mean_ndvi", height=6, aspect=1.2)
# plt.title("Scatterplot: Temperature vs NDVI")
# plt.xlabel("Mean Temperature (°C)")
# plt.ylabel("Mean NDVI")
# plt.show()


###########################################################

#plt.figure(figsize=(12, 6))
# Select a few key states
# selected_states = ["DEBY"]

# for state in selected_states:
#     state_data = merged_df[merged_df["State"] == state]
#     sns.lineplot(data=state_data, x="Year", y="mean_ndvi", label=f"NDVI - {state}")
#     sns.lineplot(data=state_data, x="Year", y="Temperature", label=f"Temp - {state}", linestyle="--")

# plt.title("NDVI & Temperature Trends Over Time (Selected States)")
# plt.xlabel("Year")
# plt.ylabel("Value")
# plt.legend()
# plt.show()

###########################################################


# plt.figure(figsize=(12, 6))
# sns.boxplot(data=merged_df, x="Year", y="mean_ndvi")
# plt.title("Yearly Distribution of NDVI")
# plt.show()

# plt.figure(figsize=(12, 6))
# sns.boxplot(data=merged_df, x="Year", y="Temperature")
# plt.title("Yearly Distribution of Temperature")
# plt.show()