import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 📂 Define file path 
merged_file = "full-analyze\\data\\merged_ndvi_precipitation.csv"  # Path to the merged dataset

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

df["precip_lag1"] = df.groupby("State")["mean_precip"].shift(1)  # Shift precipitation by 1 year
lagged_corr = df[["precip_lag1", "mean_ndvi"]].corr()
print(lagged_corr)


state_lagged_corr = df.groupby("State")[["precip_lag1", "mean_ndvi"]].corr().unstack().iloc[:, 1]
print(state_lagged_corr)