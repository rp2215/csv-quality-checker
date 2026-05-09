from csv_loader import load_csv
from quality_check import run_quality_checks
from report_generator import display_report, display_batch_report, save_markdown_report, save_batch_markdown_reports
from batch_processor import process_csv_folder
from pathlib import Path


def main():

    input_path = Path("data")
    
    if input_path.is_dir():
        batch_results = process_csv_folder(input_path)
        display_batch_report(batch_results)

    elif input_path.is_file():
        dataframe = load_csv(input_path)
        results = run_quality_checks(dataframe)
        display_report(results,input_path.name)
    
    else:
        print(f"Input path does not exist: {input_path}")

if __name__ == "__main__":
    main()
