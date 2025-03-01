import os
import shutil

def move_files_by_year(source_folder, dest_base_folder):
    """
    Moves files from source_folder to sub-folders in dest_base_folder based on the year in the filename.
    The filename is expected to have underscore-separated parts, with the first date at index 3.
    
    For example:
      LC08_L2SP_196026_20210808_20220818_02_T1_SR_B5 will be moved to the '2021' folder.
      LC08_L2SP_196026_20000906_20101111_02_T1_SR_B5 will be moved to the '2000' folder.
    """
    # Iterate over all items in the source folder
    for filename in os.listdir(source_folder):
        file_path = os.path.join(source_folder, filename)
        # Process only files (skip directories, etc.)
        if os.path.isfile(file_path):
            parts = filename.split('_')
            if len(parts) > 3:  # Ensure there are at least 4 parts
                date_str = parts[3]
                if len(date_str) >= 4:
                    year = date_str[:4]
                    # Construct the destination folder path based on the year
                    target_folder = os.path.join(dest_base_folder, year)
                    os.makedirs(target_folder, exist_ok=True)
                    
                    dest_file = os.path.join(target_folder, filename)
                    
                    # Move the file to the target folder
                    shutil.move(file_path, dest_file)
                    # Print success with a green tick and the filename
                    print(f"✅ {filename}")
                else:
                    # Print error with a red cross and the filename
                    print(f"❌ {filename} (date string is too short)")
            else:
                # Print error with a red cross and the filename
                print(f"❌ {filename} (filename does not have enough parts)")


if __name__ == '__main__':
    # Define the source directory and destination base directory.
    # Modify these paths as needed.
    source_folder = 'C:\\Users\\M0H3N\\Downloads\\2012-2013-usgs'
    dest_base_folder = 'C:\\Users\\M0H3N\\Downloads\\USGS'
    
    move_files_by_year(source_folder, dest_base_folder)
