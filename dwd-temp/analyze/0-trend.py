import os
import pandas as pd
import matplotlib.pyplot as plt

# Folder containing the CSV files
csv_folder = "dwd-temp\\data\\1-final-data-state-name"

# Get all CSV files
csv_files = sorted([f for f in os.listdir(csv_folder) if f.endswith(".csv")])

# Prepare a list to store yearly mean temperature data
yearly_mean_temp = []

for file in csv_files:
    file_path = os.path.join(csv_folder, file)
    year = file.split("_")[-1].split(".")[0]  # Extract year from filename
    
    # Load CSV
    df = pd.read_csv(file_path)
    
    # Calculate mean temperature across all states
    mean_temp = df["Mean_Temperature (°C)"].mean()
    
    # Store year and mean temperature
    yearly_mean_temp.append({"Year": int(year), "Mean_Temperature": mean_temp})

# Convert to DataFrame
df_trend = pd.DataFrame(yearly_mean_temp)

# Sort by Year (just in case)
df_trend = df_trend.sort_values("Year")

# Plot the yearly trend
plt.figure(figsize=(10, 6))
plt.plot(df_trend["Year"], df_trend["Mean_Temperature"], marker="o", linestyle="-", color="y", label="Mean Temperature")

# Customize the plot
plt.xlabel("Year", fontsize=12)
plt.ylabel("Mean Temperature (°C)", fontsize=12)
plt.title("Yearly Trend of Mean Temperature in Germany", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.xticks(rotation=45)

# Save and show plot
plt.savefig("yearly_temperature_trend.png", dpi=300, bbox_inches="tight")
plt.show()

print("\n✅ Trend plot saved as 'yearly_temperature_trend.png'")
