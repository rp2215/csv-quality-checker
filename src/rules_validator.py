import json
from pathlib import Path
import pandas as pd
import re # used for regex pattern validation

# Load and validate contents of JSON rules file
def load_rules_file(rules_file_path):

    path = Path(rules_file_path)

    # Validate file path
    if not path.exists():
        raise FileNotFoundError(f"Rules file not found at: {rules_file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path for rules is not a file: {rules_file_path}")
    
    if path.suffix.lower() != ".json":
        raise ValueError("Rules file must be a .json file")
    
    if path.stat().st_size == 0:
        raise ValueError(f"Rules file is empty: {rules_file_path}")
    
    # Open and read JSON file
    with path.open("r", encoding="utf-8") as rules_file:
        rules = json.load(rules_file)

    # Validate contents of JSON file
    if "columns" not in rules:
        raise ValueError("Rules file must contain a 'columns' section")
    
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

# Check whether column is required or optional
def check_required_column(dataframe, column_name, column_rules):

    required = column_rules.get("required", True)
    column_exists = column_name in dataframe.columns # check if name in df

    # pass
    if column_exists:
        return build_check_result(
            "required",
            True,
            "Column exists",
        )
    
    # fail if missing and required
    if required:
        return build_check_result(
            "required",
            False,
            "Required Column is missing",
        )

    # pass if column missing but optional
    return build_check_result(
            "required",
            True,
            "Optional column is missing",
        )

# missing value percentage for one column
def calculate_column_missing_percentage(dataframe, column_name):

    missing_percentage = dataframe[column_name].isnull().mean() * 100

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
    
    expected_type = str(column_rules["type"]).strip().lower() 

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
        "No invalid integer values found"
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
        "No invalid date values found"
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
        "No invalid boolean values found"
        )
    
    # int or decimal
    if expected_type == "number":

        numeric_series = pd.to_numeric(series, errors="coerce")
        invalid_count = int(numeric_series.isnull().sum())

        # fail 
        if invalid_count >=1 :
            return build_check_result(
                "type",
                False,
                f"Invalid numeric values found: {invalid_count}"
            )
        
        # all values converted successfully
        return build_check_result(
            "type",
            True,
            "No invalid numeric values found"
        )
    
    # CSV values all string so text will always pass
    if expected_type == "text":

        return build_check_result(
            "type",
            True,
            "All values are text"
        )
    
    # fallback for types not supported (yet)
    return build_check_result(
        "type",
        False,
        f"Unsupported type rule: {expected_type}",
    )

# check against min/max value rules
def check_numeric_range(dataframe, column_name, column_rules):

    if "min" not in column_rules and "max" not in column_rules:
        return None
    
    series = dataframe[column_name].dropna() # ignore missing value for check
    numeric_series = pd.to_numeric(series, errors="coerce")

    invalid_numbers_count = int(numeric_series.isnull().sum()) # values that coudlnt be converted

    # fail
    if invalid_numbers_count > 0:
        return build_check_result("numeric_range", False, f"Non numeric values found: {invalid_numbers_count}")

    invalid_range_count = 0

    if "min" in column_rules:

        below_min_count = int((numeric_series < column_rules["min"]).sum())
        invalid_range_count = invalid_range_count + below_min_count

    if "max" in column_rules:

        above_max_count = int((numeric_series > column_rules["max"]).sum())
        invalid_range_count = invalid_range_count + above_max_count
    
    # fail
    if invalid_range_count >= 1:
        return build_check_result("numeric_range", False, f"Number of values outside allowed range: {invalid_range_count}")

    # pass
    return build_check_result("numeric_range", True, "All values are within allowed range",)

# check that all values in a column match a user-defined regex pattern (email, postcodes etc)
def check_pattern(dataframe, column_name, column_rules):

    # rule not provided
    if "pattern" not in column_rules:
        return None

    pattern = column_rules["pattern"]

    # check pattern is valid regex before applying
    try:
        compiled_pattern = re.compile(pattern)
    except re.error:
        return build_check_result(
            "pattern",
            False,
            f"Invalid regex pattern: {pattern}"
        )

    series = dataframe[column_name].dropna().astype(str)
    is_invalid = series.apply(lambda value: compiled_pattern.fullmatch(value) is None)

    invalid_count = int(is_invalid.sum())

    # fail
    if invalid_count >= 1:
        return build_check_result(
            "pattern",
            False,
            f"Values not matching pattern '{pattern}': {invalid_count}"
        )

    return build_check_result(
        "pattern",
        True,
        f"All values match pattern '{pattern}'"
    )


# check against allowed values rules
def check_allowed_values(dataframe, column_name, column_rules):

    if "allowed_values" not in column_rules:
        return None
    
    allowed_values = column_rules["allowed_values"]

    # check allowed_values is a list
    if not isinstance(allowed_values, list):
        return build_check_result("allowed_values", False, "Specified allowed values must be a list")
    
    series = dataframe[column_name].dropna()

    is_valid_value = series.isin(allowed_values)
    is_invalid_value = ~is_valid_value

    invalid_count = int(is_invalid_value.sum())

    # fail
    if invalid_count >= 1:
        return build_check_result("allowed_values", False, f"Number of values outside allowed list: {invalid_count}")
    
    # pass
    return build_check_result("allowed_values", True, "All values are in the allowed list")

# check that all non-null values in the column are unique (no duplicates)
def check_unique(dataframe, column_name, column_rules):

    if not column_rules.get("unique", False):
        return None

    series = dataframe[column_name].dropna()  # null values are ignored — they don't count as duplicates

    # keep=False marks every copy of a duplicated value as True, not just the second occurrence
    duplicate_mask = series.duplicated(keep=False)
    duplicate_count = int(duplicate_mask.sum())

    if duplicate_count >= 1:
        return build_check_result(
            "unique",
            False,
            f"Duplicate values found: {duplicate_count} affected rows"
        )

    return build_check_result(
        "unique",
        True,
        "All values are unique"
    )


# check that date values in a column fall within a specified date range
def check_date_range(dataframe, column_name, column_rules):

    # skip if neither bound is provided
    if "date_min" not in column_rules and "date_max" not in column_rules:
        return None

    series = dataframe[column_name].dropna()  # missing values are ignored

    # attempt to parse all present values as dates
    date_series = pd.to_datetime(series, errors="coerce")
    unparseable_count = int(date_series.isnull().sum())

    # fail early if any values can't be parsed — they can't be range-checked
    if unparseable_count > 0:
        return build_check_result(
            "date_range",
            False,
            f"Non-date values found that cannot be range-checked: {unparseable_count}"
        )

    out_of_range_count = 0

    # check lower bound if provided
    if "date_min" in column_rules:
        date_min = pd.to_datetime(column_rules["date_min"])  # parse the rule value itself to datetime
        out_of_range_count += int((date_series < date_min).sum())

    # check upper bound if provided
    if "date_max" in column_rules:
        date_max = pd.to_datetime(column_rules["date_max"])  # parse the rule value itself to datetime
        out_of_range_count += int((date_series > date_max).sum())

    if out_of_range_count >= 1:
        return build_check_result(
            "date_range",
            False,
            f"Date values outside allowed range: {out_of_range_count}"
        )

    return build_check_result(
        "date_range",
        True,
        "All date values are within the allowed range"
    )


# Check if a column pass/fails for all given rules
def validate_column_rules(dataframe, column_name, column_rules):

    # result structure
    column_result = {
        "passed": True,
        "checks": [],
    }

    # Perform required columns rules and store results
    required_column_result = check_required_column(dataframe, column_name, column_rules)
    column_result["checks"].append(required_column_result)

    # cant proceed to other rule checks if doesnt exist stop early
    if not required_column_result["passed"]:
        column_result["passed"] = False
        return column_result
    
    # column is optional and missing stop without failing
    if column_name not in dataframe.columns:
        return column_result
    
    column_validation_checks = [
        check_missing_percentage,
        validate_type,
        check_numeric_range,
        check_allowed_values,
        check_pattern,
        check_unique,
        check_date_range,
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
        "columns": {},
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
