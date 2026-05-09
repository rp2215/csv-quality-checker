# Load One CSV File

import pandas as pd
from pathlib import Path

# load CSV file from given file path
def load_csv(file_path):
    
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found at: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path  {file_path} is not a file")
    
    if path.suffix.lower() != ".csv":
        raise ValueError(f"File must be a CSV file")
    
    if path.start().st.size == 0:
        raise ValueError(f"CSV file is empty: {file_path}")
    
    dataframe = pd.read_csv(path)

    return dataframe
