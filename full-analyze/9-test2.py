import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 📂 Define file path
merged_file = "full-analyze\\data\\merged_ndvi_sunshine.csv"  # Path to the merged dataset

# 📌 Load the merged dataset
df = pd.read_csv(merged_file)

# 🔄 State Mapping Dictionary (Codes → Full Names)
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
    "DETH": "Thuringia"
}

# 📌 Replace state codes with full names
df["State"] = df["State"].map(state_mapping)

# 📌 Pivot the data for heatmaps (States as rows, Years as columns)
sunshine_pivot = df.pivot(index="State", columns="Year", values="Mean_Sunshine")


# 🔥 Plot Sunshine Heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(sunshine_pivot, cmap="YlOrBr", linewidths=0.5, annot=False)
plt.title("Sunshine Heatmap (State vs Year)")
plt.xlabel("Year")
plt.ylabel("State")
plt.xticks(rotation=45)  # Rotate year labels for readability
# plt.savefig("Sunshine_heatmap.png", dpi=300, bbox_inches="tight")
plt.show()

print("\n✅ Heatmap saved: Sunshine_heatmap.png")
