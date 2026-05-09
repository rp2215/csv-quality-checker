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

# Runs all quality checks and stores in dictionary
def run_quality_checks(dataframe):
    
    results = {
        "row_count": count_rows(dataframe),
        "column_count": count_columns(dataframe),
        "column_names": get_column_names(dataframe),
        "missing_values": count_missing_values(dataframe),
        "duplicate_rows": count_duplicate_rows(dataframe),
        "data_types": get_data_types(dataframe),
    }

    return results
