# Process Many CSV File Found In A Folder

from pathlib import Path
from csv_loader import load_csv
from quality_check import run_quality_checks


# Finds every CSV file inside a folder
def find_csv_files(folder_path):

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f" Folder Not Found: {folder_path}")
    
    if not folder.is_dir():
        raise ValueError(f"Path is not a folder: {folder_path}")
    
    csv_files = sorted(folder.glob("*.csv")) # find every file with .csv extension

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in folder: {folder_path}")
    
    return csv_files

# Process One CSV File
def process_single_csv(file_path):

    # Dict to store files results
    file_result = {
        "file_name": Path(file_path).name,
        "file_path": str(file_path),
        "status": "success",
        "results": None,
        "error": None,
    }

    # try and load and analyse file
    try:
        dataframe = load_csv(file_path)

        results = run_quality_checks(dataframe)

        file_result["results"] = results

    # Catch errors that occur during processing
    except Exception as error:

        file_result["status"] = "failed"

        file_result["error"] = str(error)

    return file_result

# Processes every CSV file in a folder
def process_csv_folder(folder_path):

    csv_files = find_csv_files(folder_path)

    batch_results = []

    # Loop through every CSV file found and process returning results
    for csv_file in csv_files:

        file_result = process_single_csv(csv_file)

        batch_results.append(file_result)

    return batch_results






    