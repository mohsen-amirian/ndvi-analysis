import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define file path (adjust if necessary)
file_path = "dwd\\0-data\\1-data-clipped-to-de-states\\merged_precipitation.csv"

df_precip_all = pd.read_csv(file_path)

# Convert 'time' column to datetime format
df_precip_all["time"] = pd.to_datetime(df_precip_all["time"])

# Extract year from time column
df_precip_all["year"] = df_precip_all["time"].dt.year

# State Mapping: Replace abbreviations with full names
state_mapping = {
    "DEBW": "Baden-Württemberg",
    "DEBY": "Bayern",
    "DEBE": "Berlin",
    "DEBB": "Brandenburg",
    "DEHB": "Bremen",
    "DEHH": "Hamburg",
    "DEHE": "Hesse",
    "DEMV": "Mecklenburg-Vorpommern",
    "DENI": "Niedersachsen",
    "DENW": "Nordrhein-Westfalen",
    "DERP": "Rheinland-Pfalz",
    "DESL": "Saarland",
    "DESN": "Sachsen",
    "DEST": "Sachsen-Anhalt",
    "DESH": "Schleswig-Holstein",
    "DETH": "Thuringia",
}

df_precip_all["state"] = df_precip_all["state"].map(state_mapping)

# Aggregate precipitation by year and state (taking the mean)
pivot_table = df_precip_all.groupby(["state", "year"])["precip"].mean().unstack()

# Plot heatmap with full state names
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, cmap="Blues", linewidths=0.5)

# Labels & Title
plt.title("Precipitation Trends by State Over Time")
plt.xlabel("Year")
plt.ylabel("State")

# Show plot
plt.show()
