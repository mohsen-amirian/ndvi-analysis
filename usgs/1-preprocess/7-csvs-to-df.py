import os
import pandas as pd

# Dictionary to map abbreviations to full state names
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

# 1️⃣ Set the folder path containing CSV files
folder_path = "usgs\\preprocess\\ndvi-csv-seasonal"  # Change this to your actual folder path

# 2️⃣ Create an empty list to store the data
all_data = []

# 3️⃣ Loop through all CSV files in the folder
for file in os.listdir(folder_path):
    if file.endswith(".csv"):
        # Extract year and season from filename (e.g., "1987_Spring_NDVI.csv")
        parts = file.split("_")
        year = int(parts[0])
        season = parts[1]

        # Load the CSV file
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)

        # Ensure correct columns exist
        if "id" in df.columns and "mean_ndvi" in df.columns:
            # Add year and season columns
            df["year"] = year
            df["season"] = season
            all_data.append(df)

# 4️⃣ Merge all data into a single DataFrame
ndvi_df = pd.concat(all_data, ignore_index=True)

# 5️⃣ Handle missing values (-9999 → NaN)
# Convert mean_ndvi to numeric (ensures it's float)
ndvi_df["mean_ndvi"] = pd.to_numeric(ndvi_df["mean_ndvi"], errors="coerce")

# Replace -9999 with NaN (Future-proof way)
ndvi_df["mean_ndvi"] = ndvi_df["mean_ndvi"].replace(-9999, pd.NA)

# Convert year to numeric
ndvi_df["year"] = pd.to_numeric(ndvi_df["year"])

# Apply mapping to your DataFrame
ndvi_df["state_name"] = ndvi_df["id"].map(state_mapping)

#Detect outliers using IQR
Q1 = ndvi_df["mean_ndvi"].quantile(0.25)
Q3 = ndvi_df["mean_ndvi"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Replace only outliers with median
median_value = ndvi_df["mean_ndvi"].median()
ndvi_df.loc[(ndvi_df["mean_ndvi"] > upper_bound) | (ndvi_df["mean_ndvi"] < lower_bound), "mean_ndvi"] = median_value

ndvi_df.to_csv('usgs\\analyze\\data\\ndvi_full_df.csv', index=False)

