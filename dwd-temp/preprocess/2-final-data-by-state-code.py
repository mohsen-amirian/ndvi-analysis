import os
import pandas as pd

# 📂 Define input & output folder paths (UPDATE THIS)
input_folder = "dwd-temp\\data\\1-final-data-state-neme"  # Folder containing original CSV files
output_folder = "dwd-temp\\data\\2-final-data-state-code"  # Folder for modified CSVs

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# 🔄 State mapping dictionary (Names → Codes)
state_mapping = {
    "Baden-Württemberg": "DEBW",
    "Bayern": "DEBY",
    "Berlin": "DEBE",
    "Brandenburg": "DEBB",
    "Bremen": "DEHB",
    "Hamburg": "DEHH",
    "Hessen": "DEHE",
    "Mecklenburg-Vorpommern": "DEMV",
    "Niedersachsen": "DENI",
    "Nordrhein-Westfalen": "DENW",
    "Rheinland-Pfalz": "DERP",
    "Saarland": "DESL",
    "Sachsen": "DESN",
    "Sachsen-Anhalt": "DEST",
    "Schleswig-Holstein": "DESH",
    "Thüringen": "DETH",
}

# 📂 Get all temperature CSV files
csv_files = sorted([f for f in os.listdir(input_folder) if f.startswith("temperature_per_state_") and f.endswith(".csv")])

# 🔄 Process each CSV file
for file in csv_files:
    file_path = os.path.join(input_folder, file)
    
    # Extract year from filename
    year = file.split("_")[-1].split(".")[0]

    # Load the CSV file
    df = pd.read_csv(file_path)

    # Replace state names with state codes
    df["State"] = df["State"].map(state_mapping)

    # Define new filename format
    new_filename = f"temperature_{year}.csv"
    output_file_path = os.path.join(output_folder, new_filename)

    # Save the modified file
    df.to_csv(output_file_path, index=False)

    print(f"✅ Saved: {output_file_path}")

print("\n✅ All temperature files updated with state codes!")
