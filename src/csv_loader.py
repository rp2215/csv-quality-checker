# Load One CSV File

import pandas as pd
from pathlib import Path
import csv
from collections import Counter

# find duplicate column names from header row
def find_duplicate_column_names(file_path):

    path = Path(file_path)
    
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file: # use sig to handle possible BOM characters

        reader = csv.reader(csv_file)
        headers= next(reader, []) # read first row as header row

    header_counts = Counter(headers) # count num times each name appears

    # list of names that appear more than once
    duplicate_column_names = [column_name for column_name, count in header_counts.items() if count > 1]

    return duplicate_column_names

# load CSV file from given file path
def load_csv(file_path):
    
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found at: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path  {file_path} is not a file")
    
    if path.suffix.lower() != ".csv":
        raise ValueError("File must be a CSV file")
    
    if path.stat().st_size == 0:
        raise ValueError(f"CSV file is empty: {file_path}")
    
    duplicate_column_names = find_duplicate_column_names(path) # detect duplicates beofre loading as pandas often renames duplicate headers
    
    dataframe = pd.read_csv(path)

    dataframe.attrs["duplicate_column_names"] = duplicate_column_names

    return dataframe
