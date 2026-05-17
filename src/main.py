from csv_loader import load_csv
from quality_check import run_quality_checks
from report_generator import display_report, display_batch_report, save_markdown_report, save_batch_markdown_reports
from batch_processor import process_csv_folder
from rules_validator import load_rules_file
from rules_validator import validate_dataframe_all_rules
from warning_generator import get_thresholds

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

    # optional report name argument
    parser.add_argument(
        "--report-name",
        default=None,
        help="Choose a custome name for the saved report"
    )

    # user can choose file of folder to analyse
    parser.add_argument(
        "--input",
        default="data",
        help="Enter path to a CSV file or folder containing CSV files",
    )

    parser.add_argument(
        "--recursive",
        action="store_true", # True when flag is used
        help="Search for CSV files inside subfolders as well"
    )

    # user can optionally add rules file to check uploaded dataset have what they require
    parser.add_argument(
        "--rules",
        default=None,
        help="Add an optional path to a JSON rules file",
    )

    return parser.parse_args()

def main():

    args = get_arguments()
    input_path = Path(args.input)
    output_folder = Path("reports")

    rules = None

    # Load rules file from user path
    if args.rules:
        rules = load_rules_file(args.rules)
    
    # check if folder
    if input_path.is_dir():

        batch_results = process_csv_folder(input_path,args.recursive,rules)

        # check what output user wants
        if args.mode in ["terminal", "both"]:
            display_batch_report(batch_results)

        if args.mode in ["download", "both"]:
            saved_reports = save_batch_markdown_reports(batch_results, output_folder, args.report_name)

            print("\n Saved Reports:")

            for report_path in saved_reports:
                print(f"- {report_path}")    

    elif input_path.is_file():

        dataframe = load_csv(input_path)
        thresholds = get_thresholds(rules)
        results = run_quality_checks(dataframe, thresholds)

        if rules:
            results["rules_validation"] = validate_dataframe_all_rules(dataframe,rules)

        else: 
            results["rules_validation"] = None

        # check what output user wants
        if args.mode in ["terminal", "both"]:
            display_report(results, input_path.name)

        if args.mode in ["download", "both"]:
            report_path = save_markdown_report(results,input_path.name, output_folder, args.report_name)

            print(f"\nReport saved to: {report_path}")

    else:
        print(f"Input path does not exist: {input_path}")

if __name__ == "__main__":
    main()