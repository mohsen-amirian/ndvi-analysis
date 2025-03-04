import os
import glob

def get_files_by_pattern(folder_path, pattern):
    return glob.glob(os.path.join(folder_path, pattern))



def list_files_in_folder(folder: str) -> list:
    """
    Returns a list of all file full names in the specified folder.
    
    Parameters:
    folder (str): The path to the folder.
    
    Returns:
    list: A list of file path (strings) in the folder.
    """
    return [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]