# Runs Checks On A DataFrame

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
def run_quality_checks(dataframe):

    overall_qaulity_score = calculate_overall_quality_score(dataframe)

    results = {
        "row_count": count_rows(dataframe),
        "column_count": count_columns(dataframe),
        "column_names": get_column_names(dataframe),
        "missing_values": count_missing_values(dataframe),
        "duplicate_rows": count_duplicate_rows(dataframe),
        "data_types": get_data_types(dataframe),
        "missing_percentage": calculate_missing_value_percentages(dataframe),
        "duplicate_percentage": calculate_duplicate_row_percentage(dataframe),
        "column_quality_scores": calculate_column_quality_scores(dataframe),
        "overall_quality_score": overall_qaulity_score,
        "overall_quality_label": get_quality_score_label(overall_qaulity_score)
    }

    return results
