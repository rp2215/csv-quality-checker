# Process Many CSV File Found In A Folder

from pathlib import Path

from csv_loader import load_csv
from quality_check import run_quality_checks
from rules_validator import validate_dataframe_all_rules

# Finds every CSV file inside a folder
def find_csv_files(folder_path, recursive=False):

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f" Folder Not Found: {folder_path}")
    
    if not folder.is_dir():
        raise ValueError(f"Path is not a folder: {folder_path}")
    
    # finds CSV files in folder and subfolders
    if recursive:
        csv_files = sorted(folder.rglob("*.csv"))

    else:
        csv_files = sorted(folder.glob("*.csv")) # find every file with .csv extension in single folder

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in folder: {folder_path}")
    
    return csv_files

# Process One CSV File
def process_single_csv(file_path, rules=None):

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

        # run rule validation if rules have been added
        if rules:
            results["rules_validation"] = validate_dataframe_all_rules(dataframe, rules)
        
        else:
            results["rules_validation"] = None

        file_result["results"] = results

    # Catch errors that occur during processing
    except Exception as error:

        file_result["status"] = "failed"

        file_result["error"] = str(error)

    return file_result

# Processes every CSV file in a folder
def process_csv_folder(folder_path, recursive=False, rules=None):

    folder = Path(folder_path)

    csv_files = find_csv_files(folder_path, recursive)

    batch_results = []

    total_files = len(csv_files)
    print(f"\nFound {total_files} CSV file(s) to process")

    # Loop through every CSV file found and process returning results wiht progress indicator
    for index, csv_file in enumerate(csv_files, start=1):

        completion_percentage = round((index / total_files) * 100)

        relative_file_path = csv_file.relative_to(folder) # folder aware file path
        
        print(f"\nProcessing file {index}/{total_files} ({completion_percentage}%): {relative_file_path}") 

        file_result = process_single_csv(csv_file,rules)
        batch_results.append(file_result)

        if file_result["status"] == "success":
            print(f"Completed file {index}/{total_files}: {relative_file_path}")  # Show success message

        else:
            # Show Failure and Error Message
            print(f"Failed file {index}/{total_files}: {relative_file_path}")  
            print(f"Error: {file_result['error']}")  

    print(f"\nBatch processing complete: {total_files}/{total_files} files checked.") 

    return batch_results