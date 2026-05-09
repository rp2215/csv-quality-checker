# displays single report in terminal
def display_report(results, file_name=None):
    
    print("\nCSV Data Quality Report")

    print("=" * 30) # seperator line

    # if file name provided
    if file_name:
        print(f"\nFile: {file_name}")

    print(f"\nRows: {results['row_count']}")

    print(f"Columns: {results['column_count']}")


    print("\nColumn Names:")

    # loop through each column name and print
    for column in results["column_names"]:
        print(f"- {column}")

    
    print("\nMissing Values:")

    # print each missing value count for each column
    for column, missing_count in results["missing_values"].items(): 
        print(f"- {column}: {missing_count}")


    print(f"\nDuplicate Rows: {results['duplicate_rows']}")

    print("\nData Types:")

    # print each data type for columns
    for column, data_type in results["data_types"].items():
        print(f"- {column}: {data_type}")

    print()

# displays multiple reports in terminal
def display_batch_report(batch_results):

    print("\nCSV Data Quality Report")

    print("=" * 30) # seperator line

    print(f"\n Num Files Processed: {len(batch_results)}")

    successful_files = sum(1 for file_result in batch_results if file_result["status"] == "success")

    failed_files = sum(1 for file_result in batch_results if file_result["status"] == "failed")

    print(f"Successfule Files: {successful_files}")

    print(f"Failed Files: {failed_files}")
    
    for file_result in batch_results:

        # if success display report
        if file_result["status"] == "success":
            display_report(file_result["results"], file_result["file_name"])

        else:
            print(f"\n Failed to process: {file_result['file_name']}")
            print(f"Error: {file_result['error']}")
            print("-" * 30)
        