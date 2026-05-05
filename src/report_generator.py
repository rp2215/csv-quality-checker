# formats and displays report in terminal
def display_report(results):
    
    print("\nCSV Data Quality Report")

    print("=" * 30)

    print(f"\nRows: {results['row_count']}")

    print(f"Columns: {results['column_count']}")


    print("\nColumn Names:")

    for column in results["column_names"]:
        print(f"- {column}")

    
    print("\nMissing Values:")

    for column, missing_count in results["missing_values"].items(): 
        print(f"- {column}: {missing_count}")

    print(f"\nDuplicate Rows: {results['duplicate_rows']}")

    print("\nData Types:")

    for column, data_type in results["data_types"].items():
        print(f"- {column}: {data_type}")
