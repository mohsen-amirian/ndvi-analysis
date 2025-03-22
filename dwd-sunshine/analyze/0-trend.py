import os
import pandas as pd
import matplotlib.pyplot as plt

# Folder containing the CSV files
csv_folder = "dwd-sunshine\\data\\1-final-data-state-name"

# Get all CSV files
csv_files = sorted([f for f in os.listdir(csv_folder) if f.endswith(".csv")])

# Prepare a list to store yearly mean sun shine data
yearly_mean_sunshine = []

for file in csv_files:
    file_path = os.path.join(csv_folder, file)
    year = file.split("_")[-1].split(".")[0]  # Extract year from filename
    
    # Load CSV
    df = pd.read_csv(file_path)
    
    # Calculate mean sunshine across all states
    mean_sunshine = df["Mean_Sunshine"].mean()
    
    # Store year and mean sunshine
    yearly_mean_sunshine.append({"Year": int(year), "Mean_Sunshine": mean_sunshine})

# Convert to DataFrame
df_trend = pd.DataFrame(yearly_mean_sunshine)

# Sort by Year (just in case)
df_trend = df_trend.sort_values("Year")

# Plot the yearly trend
plt.figure(figsize=(10, 6))
plt.plot(df_trend["Year"], df_trend["Mean_Sunshine"], marker="o", linestyle="-", color="r", label="Mean SunShine")

# Customize the plot
plt.xlabel("Year", fontsize=12)
plt.ylabel("Mean SunShine (Hours per month)", fontsize=12)
plt.title("Yearly Trend of Mean SunShine in Germany", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend()
plt.xticks(rotation=45)

# Save and show plot
#plt.savefig("yearly_sunshine_trend.png", dpi=300, bbox_inches="tight")
plt.show()
