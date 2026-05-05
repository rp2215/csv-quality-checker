from csv_loader import load_csv
from quality_check import run_quality_checks
from report_generator import display_report

# test the CSV loader
def main():

    file_path = "data/test.csv"

    dataframe = load_csv(file_path)

    results = run_quality_checks(dataframe)

    #print(dataframe.head())

    display_report(results)


if __name__ == "__main__":
    main()
