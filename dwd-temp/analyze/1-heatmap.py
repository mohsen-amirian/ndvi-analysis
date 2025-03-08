import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Folder containing the CSV files
csv_folder = "dwd-temp\\data\\output_csv"

# Get all CSV files
csv_files = sorted([f for f in os.listdir(csv_folder) if f.endswith(".csv")])

# Load and merge all CSVs into a single DataFrame
all_data = []

for file in csv_files:
    file_path = os.path.join(csv_folder, file)
    year = file.split("_")[-1].split(".")[0]  # Extract year from filename
    
    # Load CSV
    df = pd.read_csv(file_path)
    df["Year"] = int(year)  # Add year column
    
    all_data.append(df)

# Combine all years into a single DataFrame
df_all = pd.concat(all_data)

# Pivot data for heatmap (states as rows, years as columns)
heatmap_data = df_all.pivot(index="State", columns="Year", values="Mean_Temperature (°C)")

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap="coolwarm", annot=False, linewidths=0.5)

# Customize plot
plt.title("Annual Mean Temperature Heatmap (°C) - German States", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("State", fontsize=12)

# Save heatmap as PNG
#plt.savefig("temperature_heatmap.png", dpi=300, bbox_inches="tight")
plt.show()

print("\n✅ Heatmap saved as 'temperature_heatmap.png'")
