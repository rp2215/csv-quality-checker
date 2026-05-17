from warning_generator import generate_warnings

def count_rows(dataframe):
    return dataframe.shape[0]

def count_columns(dataframe):
    return dataframe.shape[1]

def get_column_names(dataframe):
    return list(dataframe.columns) 

def count_missing_values(dataframe):
    return dataframe.isnull().sum().to_dict()

def count_duplicate_rows(dataframe):
    return dataframe.duplicated().sum()

def get_data_types(dataframe):
    return dataframe.dtypes.astype(str).to_dict() # convert to string return as dict


def calculate_missing_value_percentages(dataframe):

    missing_percentage = dataframe.isnull().mean() * 100 
    return missing_percentage.round(2).to_dict()

def calculate_duplicate_row_percentage(dataframe):

    total_rows = count_rows(dataframe)

    if total_rows ==0:
        return 0
    
    duplicate_percentage = (count_duplicate_rows(dataframe)/ total_rows) * 100

    return round(duplicate_percentage,2)

# get duplicate names detected from in csv_loader.py 
def detect_duplicate_column_names(dataframe):
    duplicate_column_names = dataframe.attrs.get("duplicate_column_names",[])
    return duplicate_column_names

# number of unique values in each column
def count_unique_values(dataframe):

    unique_counts = dataframe.nunique(dropna=True) # ignores missing values

    return unique_counts.to_dict()

# count rows where every value is missing
def count_empty_rows(dataframe):

    missing_values = dataframe.isnull() # missing values marked as True

    empty_row_count = sum(missing_values.all(axis=1))

    return int(empty_row_count)

# count columns where every value is missing 
def detect_empty_columns(dataframe):

    empty_columns = []

    for column in dataframe.columns:

        missing_values = dataframe[column].isnull()
        column_is_empty = missing_values.all()

        if column_is_empty:
            empty_columns.append(column)

    return empty_columns

# generates min, max, mean, median for numeric columns
def get_numeric_summaries(dataframe):

    numeric_dataframe = dataframe.select_dtypes(include="number")

    numeric_summaries = {}

    for column in numeric_dataframe.columns:

        series = numeric_dataframe[column]

        numeric_summaries[column] = {

            "min": round(float(series.min()), 2),
            "max": round(float(series.max()),2),
            "mean": round(float(series.mean()),2),
            "median":round(float(series.median()),2),
        }
    return numeric_summaries


def calculate_column_quality_scores(dataframe):

    missing_percentages = calculate_missing_value_percentages(dataframe)

    column_scores = {}

    for column, missing_percentage in missing_percentages.items():

        score = 100 - missing_percentage
        score = max(score,0) # score cant be below 0
        score = round(score, 2)
        column_scores[column] = score

    return column_scores

def calculate_overall_quality_score(dataframe):

    column_scores = calculate_column_quality_scores(dataframe)

    if not column_scores:
        return 0 # file cant be scored if no column scores
    
    average_column_score = sum(column_scores.values()) / len(column_scores)

    duplicate_penalty = calculate_duplicate_row_percentage(dataframe)

    overall_file_quality_score = average_column_score - duplicate_penalty
    overall_file_quality_score = max(overall_file_quality_score, 0) # cant be below 0
    overall_file_quality_score = min(overall_file_quality_score, 100) # cant be over 100

    return round(overall_file_quality_score,2)

# Convert numeric score into a quality label
def get_quality_score_label(score):

    if score >= 90:
        return "Excellent"
 
    elif score >= 75:       
        return "Good"

    elif score >= 50:
        return "Needs Review"

    else:
        return "Poor"

# Runs all quality checks and stores in dictionary
def run_quality_checks(dataframe, thresholds = None):

    overall_quality_score = calculate_overall_quality_score(dataframe)

    results = {
        "row_count": count_rows(dataframe),
        "column_count": count_columns(dataframe),
        "column_names": get_column_names(dataframe),
        "missing_values": count_missing_values(dataframe),
        "duplicate_rows": count_duplicate_rows(dataframe),
        "data_types": get_data_types(dataframe),
        "missing_percentage": calculate_missing_value_percentages(dataframe),
        "duplicate_percentage": calculate_duplicate_row_percentage(dataframe),
        "unique_values": count_unique_values(dataframe),
        "numeric_summaries": get_numeric_summaries(dataframe),
        "empty_rows": count_empty_rows(dataframe),
        "empty_columns": detect_empty_columns(dataframe),
        "duplicate_column_names": detect_duplicate_column_names(dataframe),
        "column_quality_scores": calculate_column_quality_scores(dataframe),
        "overall_quality_score": overall_quality_score,
        "overall_quality_label": get_quality_score_label(overall_quality_score)
    }

    results["warnings"] = generate_warnings(results, thresholds) # store generated warnings

    return results
