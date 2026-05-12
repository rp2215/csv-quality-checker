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

# check against max allowed missing percentage rules

# check against expected type rules

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
        # add once implemented other rule checks
    ]

    # go through each validation check

    # return column result

# can add function to validate an entire df against all rules


