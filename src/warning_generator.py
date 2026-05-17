# Generates warning messages based on quality check results

SEVERITY_LEVELS = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

# default thresholds used when no custom values provided
DEFAULT_THRESHOLDS = {

    "missing_critical": 100,     
    "missing_high": 50,         
    "missing_medium": 25,        
    "missing_low": 10,           
    "quality_critical": 25,      
    "quality_high": 50,          
    "quality_medium": 75,       
    "low_variation_percent": 5,  
}

# merges default thresholds with user specified values
def get_thresholds(rules=None):

    # no user values provided keep default values
    if not rules:
        return DEFAULT_THRESHOLDS.copy()
    
    user_thresholds = rules.get("thresholds",{})

    # spread defaults and then overlay any user values on conflict user values wins
    return {** DEFAULT_THRESHOLDS, **user_thresholds}

# empty warning dictionary with one empty list for each level
def create_empty_warnings():

    return {
        "CRITICAL":[],
        "HIGH":[],
        "MEDIUM":[],
        "LOW":[],
    }

# add a warning message to dictionary
def add_warning(warnings, severity, message):

    if severity in warnings:
        warnings[severity].append(message)


# generate warnings for missing values
def check_missing_values_warnings(results, warnings, thresholds=None):

    # fall back to defaults
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    missing_percentages = results.get("missing_percentage",{})

    # generate warning for each column based on missing value percentage
    for column, missing_percentage in missing_percentages.items():

        if missing_percentage >= thresholds["missing_critical"]:
            add_warning(warnings, "CRITICAL", f"Column '{column}' has {missing_percentage}% missing values.")

        elif missing_percentage > thresholds["missing_high"]:
            add_warning(warnings, "HIGH", f"Column '{column}' has {missing_percentage}% missing values.")

        elif missing_percentage > thresholds["missing_medium"]:
            add_warning(warnings, "MEDIUM", f"Column '{column}' has {missing_percentage}% missing values.")

        elif missing_percentage > thresholds["missing_low"]:
            add_warning(warnings, "LOW", f"Column '{column}' has {missing_percentage}% missing values.")

# generate warnings for duplicated rows
def check_duplicate_row_warnings(results,warnings):

    duplicate_rows = results.get("duplicate_rows",0)
    duplicate_percentage = results.get("duplicate_percentage",0)

    if duplicate_rows > 0:
        add_warning(warnings, "MEDIUM", f"Dataset contains {duplicate_rows} duplicate rows ({duplicate_percentage}%)")


# generate warnings for empty rows
def check_empty_row_warnings(results,warnings):

    empty_rows = results.get("empty_rows",0)

    if empty_rows > 0:
        add_warning(warnings, "MEDIUM", f"Dataset contains {empty_rows} completely empty rows ")

# generate warnings for empty columns.
def check_empty_column_warnings(results, warnings):

    empty_columns = results.get("empty_columns", [])

    for column in empty_columns:
        add_warning(warnings, "CRITICAL", f"Column '{column}' is completely empty.")


# generate warnings for duplicate column names
def check_duplicate_column_name_warnings(results, warnings):
    
    duplicate_column_names = results.get("duplicate_column_names", [])


    for column in duplicate_column_names:
        add_warning(warnings, "HIGH", f"Duplicate column name found: '{column}'.")
                

# generate warnings for columns with unusual uniqe value patterns
def check_unique_value_warnings(results, warnings, thresholds):

    # fall back to default
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS
   
    unique_values = results.get("unique_values", {})
    row_count = results.get("row_count", 0)
    missing_values = results.get("missing_values",{})

    if row_count ==0:
        return 
    
    for column, unique_count in unique_values.items():
        
        missing_count = missing_values.get(column,0) # missing values for current column
        present_count = row_count - missing_count

        # no usable values
        if present_count == 0:
            continue

        unique_percentage = (unique_count/ present_count) * 100
        unique_percentage = round(unique_percentage,2)

        if unique_count == 1:
            add_warning(warnings,"MEDIUM", f"Column '{column}' has only 1 unique value across {present_count} present rows")

        elif unique_percentage <= thresholds["low_variation_percent"]:
            add_warning(warnings,"LOW", f"Column '{column}' has low variation: {unique_count} unique values across the present {present_count} rows ({unique_percentage}%)")


# generate warnings for overall file quality score
def check_overall_quality_warnings(results, warnings, thresholds=None):

    # fallback to default
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    overall_quality_score = results.get("overall_quality_score", 100)

    if overall_quality_score < thresholds["quality_critical"]:
        add_warning(warnings, "CRITICAL", f"Overall file quality score is low: {overall_quality_score}%.")

    elif overall_quality_score < thresholds["quality_high"]:
        add_warning(warnings, "HIGH", f"Overall file quality score needs review: {overall_quality_score}%.")

    elif overall_quality_score < thresholds["quality_medium"]:
        add_warning(warnings, "MEDIUM", f"Overall file quality score needs review: {overall_quality_score}%.")

# check if any warnings exists
def has_warnings(warnings):
  
    for severity in SEVERITY_LEVELS:
        if warnings[severity]:
            return True # if at least one

    return False

# generate all warnings form results of quality check
def generate_warnings(results, thresholds = None):

    # fallback to defaults
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS
   
    warnings = create_empty_warnings()

    check_missing_values_warnings(results, warnings, thresholds)
    check_duplicate_row_warnings(results, warnings)
    check_empty_row_warnings(results, warnings)
    check_empty_column_warnings(results, warnings)
    check_duplicate_column_name_warnings(results, warnings)
    check_unique_value_warnings(results, warnings, thresholds)
    check_overall_quality_warnings(results, warnings, thresholds)

    return warnings