import json
from pathlib import Path
import pandas as pd

# Load and validate contents of JSON rules file
def load_rules_file(rules_file_path):

    path = Path(rules_file_path)

    # Validate file path
    if not path.exists():
        raise FileNotFoundError(f"Rules file not found at: {rules_file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path for rules is not a file: {rules_file_path}")
    
    if path.suffix.lowe() != "json":
        raise ValueError("Rules file must be a .json file")
    
    if path.stat().st_size == 0:
        raise ValueError(f"Rules file is empty: {rules_file_path}")
    
    # Open and read JSON file
    with path.open("r", encoding="utf-8") as rules_file:
        rules = json.load(rules)

    # Validate contents of JSON file
    if "columns" not in rules:
        raise ValueError(f"Rules file must contain a 'columns' section")
    
    if not isinstance(rules["columns"],dict):
        raise ValueError("'columns' section of JSON file must be a dictionary")
    
    return rules

# Build dictionary result for one check of a rule
def build_check_result(rule_name, passed, message):

    return {
        "rule": rule_name,
        "passed": passed,
        "message": message
    }

# Check for required column rules retuning dict with pass/fail
def check_required_column(dataframe, column_name):

    column_exists = column_name in dataframe.columns # check if name in df

    # pass
    if column_exists:
        return build_check_result(
            "required",
            True,
            "Column exists",
        )
    
    # fail
    return build_check_result(
        "required",
        False,
        "Column is missing",
    )

# missing value percentage for one column
def calculate_column_missing_percentage(dataframe, column_name):

    missing_percentage = dataframe[column_name].isnull().mean * 100

    return round(float(missing_percentage), 2)

# check if valid missing percentag according to specified rule perent
def check_missing_percentage(dataframe, column_name, column_rules):

    # rule not provided
    if "max_missing_percent" not in column_rules:
        return None
    
    max_missing_percent = column_rules["max_missing_percent"]

    actual_missing_percent = calculate_column_missing_percentage(dataframe, column_name)

    # pass 
    if actual_missing_percent <= max_missing_percent:
        return build_check_result(
            "max_missing_percent",
            True,
            "Missing percentage is within specified limit"
        )
    else:
        return build_check_result(
            "max_missing_percent",
            False,
            "Missing percentage is too high"
        )
    
# check values match expected type
# initially only going to allow type checking of integer, date, boolean (EXPAND LATER) 
# all CSV values originally text 
def validate_type(dataframe, column_name,column_rules):

    # rule not provided
    if "type" not in column_rules:
        return None
    
    expected_type = column_rules["type"]

    # ignore missing values
    series = dataframe[column_name].dropna()

    # pass if no type to check, none are technically wrong
    if series.empty:
        return build_check_result(
            "type",
            True,
            "No present values to type check"
        )
    
    # whole numbers only
    if expected_type == "integer":

        numeric_series = pd.to_numeric(series, errors="coerce") 

        # keep only values that could be converted
        invalid_numbers = numeric_series.isnull() 
        valid_numbers = numeric_series.dropna()

        # if decimal(remainder) dont keep
        decimal_values = valid_numbers % 1 != 0

        invalid_count = int(invalid_numbers.sum() + decimal_values.sum())

        if invalid_count >= 1:
            return build_check_result(
                "type",
                False,
                f"Invalid integer values found: {invalid_count}"
            )
        
        return build_check_result(
        "type",
        True,
        f"No invalid integer values found"
    )

    if expected_type == "date":

        date_series = pd.to_datetime(series, errors="coerce")

        invalid_count = int(date_series.isnull().sum())

        if invalid_count >= 1:
            return build_check_result(
                "type",
                False,
                f"Invalid date values found: {invalid_count}"
            )
        
        return build_check_result(
        "type",
        True,
        f"No invalid date values found"
        )
    
    # values must match defined list of formats
    if expected_type == "boolean":

        boolean_series = series.astype(str).str.strip().str.lower() # convert to lowercase text for comparison

        allowed_boolean_values = {
            "true",
            "false",
            "yes",
            "no",
            "1",
            "0",
        }


        is_valid_boolean = boolean_series.isin(allowed_boolean_values)

        # flip valid results to get invalid
        is_invalid_boolean = ~is_valid_boolean
        invalid_count = int(is_invalid_boolean.sum())

        if invalid_count >= 1:
            return build_check_result(
                "type",
                False,
                f"Invalid boolean values found: {invalid_count}"
            )
        
        return build_check_result(
        "type",
        True,
        f"No invalid boolean values found"
        )
    
    # fallback for types not supported (yet)
    return build_check_result(
        "type",
        False,
        f"Unsupported type rule: {expected_type}",
    )

# check against min/max value rules

# check against allowed values rules



# Check if a column pass/fails for all given rules
def validate_column_rules(dataframe, column_name, column_rules):

    # result structure
    column_result = {
        "passed": True,
        "checks": [],
    }

    # Perform required columns rules and store results
    required_column_result = check_required_column(dataframe, column_name)
    column_result["checks"].append(required_column_result)

    # cant proceed to other rule checks if doesnt exist stop early
    if not required_column_result["passed"]:
        column_result["passed"] == False
        return column_result
    
    column_validation_checks = [
        check_missing_percentage,
        validate_type,
    ]

    for column_validation_check in column_validation_checks:

        check_result = column_validation_check(dataframe, column_name, column_rules)

        # skip check not configured
        if check_result is None:
            continue

        column_result["checks"].append(check_result)

        # mark column as fail
        if not check_result["passed"]:
            column_result["passed"] = False
        
        return column_result

# validate df using all rules
def validate_dataframe_all_rules(dataframe, rules):

    dataframe_validation_result = {
        "overall_passed": True,
        "column": {},
    }

    column_rules = rules.get("columns", {})

    for column_name, rules_for_column in column_rules.items():

        # run column checks and store
        column_result = validate_column_rules(dataframe, column_name, rules_for_column)
        dataframe_validation_result["columns"][column_name] = column_result

        # if one column fails entire df fails
        if not column_result["passed"]:
            dataframe_validation_result["overall_passed"] = False
    
    return dataframe_validation_result
