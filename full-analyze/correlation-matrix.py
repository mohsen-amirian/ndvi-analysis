import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the merged dataset (Temperature, NDVI, Precipitation for all states & years)
data_path = "path/to/merged_data.csv"  # Ensure you have all three variables in a single dataset
df = pd.read_csv(data_path)

# Compute Correlation Matrix
correlation_matrix = df[['Mean_Temperature (°C)', 'NDVI', 'Precipitation']].corr(method="pearson")

# Plot Correlation Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5, fmt=".2f")
plt.title("Correlation Matrix: Temperature, NDVI, and Precipitation")
plt.savefig("correlation_heatmap.png", dpi=300, bbox_inches="tight")
plt.show()

# Pairplot (Scatterplot Matrix)
sns.pairplot(df[['Mean_Temperature (°C)', 'NDVI', 'Precipitation']], diag_kind="kde")
plt.savefig("pairplot_variables.png", dpi=300, bbox_inches="tight")
plt.show()
