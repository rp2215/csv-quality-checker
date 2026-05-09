from csv_loader import load_csv
from quality_check import run_quality_checks
from report_generator import display_report, display_batch_report, save_markdown_report, save_batch_markdown_reports
from batch_processor import process_csv_folder
from pathlib import Path
import argparse

# collects cli arguments used for mode selection
def get_arguments():

    parser = argparse.ArgumentParser(description="CSV Data Quality Checker")

    # add mode arguments allowing selection of how report is handled
    parser.add_argument(
        "--mode",
        choices=["terminal","download","both"],
        default="terminal",
        help="Choose whehter to show report in the terminal, save as file, or both",
    )

    return parser.parse_args()

def main():

    args = get_arguments()
    input_path = Path("data")
    output_folder = Path("reports")
    
    # check if folder
    if input_path.is_dir():
        batch_results = process_csv_folder(input_path)

        # check what output user wants
        if args.mode in ["terminal", "both"]:
            display_batch_report(batch_results)

        if args.mode in ["download", "both"]:
            saved_reports = save_batch_markdown_reports(batch_results, output_folder)

            print("\n Saved Reports:")

            for report_path in saved_reports:
                print(f"- {report_path}")    

    elif input_path.is_file():
        dataframe = load_csv(input_path)
        results = run_quality_checks(dataframe)

        # check what output user wants
        if args.mode in ["terminal", "both"]:
            display_report(results, input_path.name)

        if args.mode in ["download", "both"]:
            report_path = save_markdown_report(results,input_path.name, output_folder)

            print(f"\nReport saved to: {report_path}")

    else:
        print(f"Input path does not exist: {input_path}")

if __name__ == "__main__":
    main()
