import os
import gzip
import shutil

# Define paths
input_folder = "dwd-temp\\data"  # Folder containing .gz files
output_folder = "dwd-temp\\data\\extracted"  # Folder to store extracted files

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process each .gz file in the input folder
for gz_file in os.listdir(input_folder):
    if gz_file.endswith(".gz"):
        gz_path = os.path.join(input_folder, gz_file)  # Full path to .gz file
        
        # Extract the contents without renaming
        with gzip.open(gz_path, 'rb') as f_in:
            # Read the first line to get the filename inside the archive
            extracted_filename = gz_file.replace(".gz", "")  # Default name
            
            # Extract and save the file
            extracted_path = os.path.join(output_folder, extracted_filename)
            with open(extracted_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        print(f"Extracted: {gz_file} -> {extracted_path}")

print("All .gz files have been extracted successfully!")
