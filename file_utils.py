# file_utils.py

import os

def get_csv_filenames():
    # List all CSV files in the current directory
    files = [f for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.csv')]
    
    if len(files) == 0:
        raise FileNotFoundError("No CSV file found in the directory.")
    
    return files  # Return all CSV files found
