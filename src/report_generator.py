from pathlib import Path 

# Should aim to replace each part of the report and .md with helper functions in future

# helper for displaying custom rule results in terminal
def display_rules_validation(results):

    rules_validation = results.get("rules_validation")

    # no rule file used
    if not rules_validation:
        return
    
    print("\nRules Validation:")

    if rules_validation["overall_passed"]:
        print("Overall Result: PASS")
    
    else:
        print("Overall Result: FAIL")
    
    for column_name, column_result in rules_validation["columns"].items():

        if column_result["passed"]:
            column_status = "PASS"
        else:
            column_status = "FAIL"

        # display overall column result
        print(f"\n{column_name}:{column_status}")

        # display outcome of each check performed
        for check in column_result["checks"]:

            if check["passed"]:
                check_status = "PASS"
            else:
                check_status = "FAIL"
            
            print(f"- {check['rule']}: {check_status}")
            print(f"- {check['message']}")
    
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
    
    print("\n Missing Value Percentages:")

    # print each missing value percentage for each column
    for column, missing_percentage in results["missing_percentage"].items(): 
        print(f"- {column}: {missing_percentage}%")
    

    print("\nUnique Values:")

    for column, unique_count in results["unique_values"].items():
        print(f"- {column}: {unique_count}")

    print(f"\nDuplicate Rows: {results['duplicate_rows']}")
    print(f"Duplicate Row Percentage: {results['duplicate_percentage']}%")

    print(f"\nEmpty Rows: {results['empty_rows']}")

    print("\nEmpty Columns:")

    if results["empty_columns"]:
        for column in results["empty_columns"]:
            print(f"- {column}")
    else:
        print("- None")

    print("\nDuplicate Column Names:")

    if results["duplicate_column_names"]:

        for column in results["duplicate_column_names"]:
            print(f"- {column}")
    else:
        print("- None")

    print("\nData Types:")

    # print each data type for columns
    for column, data_type in results["data_types"].items():
        print(f"- {column}: {data_type}")


    print("\n Numeric Summaries:")

    if results["numeric_summaries"]:
        for column, summary in results["numeric_summaries"].items():
            print(f"\n {column}:")
            print(f"- Min: {summary['min']}")

            print(f"- Max: {summary['max']}")

            print(f"- Mean: {summary['mean']}")

            print(f"- Median: {summary['median']}")
    else:
        print("- No numeric columns found")


    print("\nColumn Quality Scores:")

    for column, score in results["column_quality_scores"].items():
        print(f"- {column}: {score}%")


    print(f"\nOverall File Quality Score: {results['overall_quality_score']}%")
    print(f"Overall File Quality {results['overall_quality_label']}")

    print("\nWarnings:")

    warnings = results.get("warnings", {})
    warnings_found = False

    # for each warning severity level print each message if exists
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:

        messages = warnings.get(severity, [])

        if messages:

            warnings_found = True
            print(f"\n{severity}:")

            for message in messages:
                print(f"- {message}")

    if not warnings_found:
        print("- No warnings found")

    display_rules_validation(results)

    print()

# displays multiple reports in terminal
def display_batch_report(batch_results):

    print("\nCSV Data Quality Report")

    print("=" * 30) # seperator line

    print(f"\n Num Files Processed: {len(batch_results)}")

    successful_files = sum(1 for file_result in batch_results if file_result["status"] == "success")

    failed_files = sum(1 for file_result in batch_results if file_result["status"] == "failed")

    print(f"Successful Files: {successful_files}")

    print(f"Failed Files: {failed_files}")
    
    for file_result in batch_results:

        # if success display report
        if file_result["status"] == "success":
            display_report(file_result["results"], file_result["file_name"])

        else:
            print(f"\n Failed to process: {file_result['file_name']}")
            print(f"Error: {file_result['error']}")
            print("-" * 30)

# helper to add the custom rule validation results to the Markdown report
def add_rules_validation_to_md_report(lines, results):

    rules_validation = results.get("rules_validation")

    # no rule file used
    if not rules_validation:
        return
    
    lines.append("## Rules Validation Results")
    lines.append("")

    if rules_validation["overall_passed"]:
        lines.append("- Overall Result: PASS")

    else:
        lines.append("- Overall Result: FAIL")

    lines.append("")

    for column_name, column_result in rules_validation["columns"].items():

        if column_result["passed"]:
            column_status = "PASS"
        
        else:
            column_status= "FAIL"
        
        lines.append(f"### {column_name}: {column_status}")
        lines.append("")

        for check in column_result["checks"]:

            if check["passed"]:
                check_status = "PASS"
            else:
                check_status = "FAIL"
            
            lines.append(f"- {check['rule']}: {check_status}")
            lines.append(f"- {check['message']}")
        
        lines.append("")

                         
# Builds .md report from quality check results
def build_markdown_report(results, file_name=None):

    lines = [] # store each line of report

    lines.append("# CSV Data Quality Report")
    lines.append("")

    if file_name:
        lines.append(f"**File:** {file_name}")
        lines.append("")

    lines.append("## Summary")
    lines.append("")

    lines.append(f"- Rows: {results['row_count']}")
    lines.append(f"- Columns: {results['column_count']}")
    lines.append(f"- Duplicate Rows: {results['duplicate_rows']}")
    lines.append(f"- Duplicate Row Percentage: {results['duplicate_percentage']}%")
    lines.append(f"- Empty Rows: {results['empty_rows']}")
    lines.append(f"- Overall File Quality Score: {results['overall_quality_score']}%")
    lines.append(f"- Overall File Quality: {results['overall_quality_label']}")

    lines.append("")

    lines.append("## Column Names")
    lines.append("")

    for column in results["column_names"]:
        lines.append(f"- {column}")

    lines.append("")

    lines.append("## Missing Values")
    lines.append("")

    for column, missing_count in results["missing_values"].items():
        lines.append(f"- {column}: {missing_count}")

    lines.append("")

    lines.append("## Missing Value Percentages")
    lines.append("")

    for column, missing_percentage in results["missing_percentage"].items():
        lines.append(f"- {column}: {missing_percentage}%")
    
    lines.append("")

    lines.append("## Unique Values")
    lines.append("")

    for column, unique_count in results["unique_values"].items():
        lines.append(f"- {column}: {unique_count}")
    
    lines.append("")

    lines.append("## Empty Columns")
    lines.append("")

    if results["empty_columns"]:
        for column in results["empty_columns"]:
            lines.append(f"- {column}")
    else:
        lines.append("- None")

    lines.append("")

    lines.append("## Duplicate Column Names")
    lines.append("")

    if results["duplicate_column_names"]:
        for column in results["duplicate_column_names"]:
            lines.append(f"- {column}")

    else:
        lines.append("- None")

    lines.append("")


    lines.append("## Data Types")
    lines.append("")

    for column, data_type in results["data_types"].items():
        lines.append(f"- {column}: {data_type}")

    lines.append("")

    lines.append("## Numeric Summaries")
    lines.append("")

    if results["numeric_summaries"]:
        for column, summary in results["numeric_summaries"].items():
            lines.append(f"### {column}")
            lines.append("")
            lines.append(f"- Min: {summary['min']}")
            lines.append(f"- Max: {summary['max']}")
            lines.append(f"- Mean: {summary['mean']}")
            lines.append(f"- Median: {summary['median']}")
            lines.append("")
    else:
        lines.append("- No numeric columns found")
        lines.append("")

    lines.append("## Column Quality Scores")
    lines.append("")

    for column, score in results["column_quality_scores"].items():
        lines.append(f"- {column}: {score}%")
    lines.append("")

    lines.append("## Warnings")
    lines.append("")

    warnings = results.get("warnings", {})
    warnings_found = False

    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:

        messages = warnings.get(severity, [])

        if messages:
            
            warnings_found = True
            lines.append(f"### {severity}")
            lines.append("")

            for message in messages:
                lines.append(f"- {message}")

            lines.append("")

    if not warnings_found:
        lines.append("- No warnings found")
        lines.append("")

    add_rules_validation_to_md_report(lines,results)

    lines.append("## Overall File Quality")
    lines.append("")

    lines.append(f"- Score: {results['overall_quality_score']}%")
    lines.append(f"- Rating: {results['overall_quality_label']}")

    lines.append("")

    return"\n".join(lines) # join all lines into one .md string

# Saves single report as .md file into reports/ folder
def save_markdown_report(results, file_name, output_folder="reports", report_name=None):

    output_path = Path(output_folder)

    output_path.mkdir(parents=True, exist_ok=True) # Create report folder if doesnt already exist

    # check if user provided custom report name
    if report_name:
        report_file_name = Path(report_name).stem + ".md"

    else:
        report_file_name = Path(file_name).stem + "_report.md" # use csv file name for report name

    report_path = output_path/report_file_name # full output file path

    # build report text and save to file
    report_text = build_markdown_report(results, file_name)
    report_path.write_text(report_text, encoding="utf-8")

    return report_path

# Saves every successful CSV file in batch result
def save_batch_markdown_reports(batch_results, output_folder="reports", report_name=None):

    saved_paths = []

    # for every file result in batch save successful ones
    for file_result in batch_results:
        if file_result["status"] == "success":

            if report_name:
                unique_batch_report_name = Path(report_name).stem + "_" + Path(file_result["file_name"]).stem
            
            # no name provided use default name
            else:
                unique_batch_report_name = None

            report_path = save_markdown_report(
                file_result["results"],
                file_result["file_name"],
                output_folder,
                unique_batch_report_name
            )

            saved_paths.append(report_path)

    return saved_paths
