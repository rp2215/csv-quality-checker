import pandas as pd
import numpy as np 

from quality_check import (
    count_rows,
    count_columns,
    count_missing_values,
    count_duplicate_rows,
    calculate_missing_value_percentages,
    calculate_duplicate_row_percentage,
    count_empty_rows,
    detect_empty_columns,
    get_numeric_summaries,
    calculate_column_quality_scores,
    calculate_overall_quality_score,
    get_quality_score_label,
)

def test_count_rows_returns_correct_count():

    # 3 row dataframe
    dataframe = pd.DataFrame({"name": ["Alice", "Bob", "Charlie"]})

    assert count_rows(dataframe) == 3


def test_count_columns_returns_correct_count():

    # 2 named columns
    dataframe = pd.DataFrame({"name": ["Alice"], "age": [30]})

    assert count_columns(dataframe) == 2


# Missing value Testing

def test_count_missing_values_detects_nulls():

    # age missing 1 value
    dataframe = pd.DataFrame({
        "name": ["Alice", "Bob"],
        "age": [30, np.nan],
    })

    result = count_missing_values(dataframe)

    assert result["name"] == 0
    assert result["age"] == 1


def test_calculate_missing_value_percentages_is_correct():

    # missing percentage 25%
    dataframe = pd.DataFrame({
        "score": [10, 20, np.nan, 40],
    })

    result = calculate_missing_value_percentages(dataframe)

    assert result["score"] == 25.0


# Duplicate value Testing

def test_count_duplicate_rows_detects_duplicates():

    # Row 3 & 1 identical
    dataframe = pd.DataFrame({
        "name": ["Alice", "Bob", "Alice"],
        "age": [30, 25, 30],
    })

    assert count_duplicate_rows(dataframe) == 1


def test_calculate_duplicate_row_percentage_is_correct():

    # duplicate percentage 25%
    dataframe = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Alice"],
        "age": [30, 25, 22, 30],
    })

    assert calculate_duplicate_row_percentage(dataframe) == 25.0


def test_calculate_duplicate_row_percentage_handles_empty_dataframe():

    # empty should return 0
    dataframe = pd.DataFrame({"name": []})

    assert calculate_duplicate_row_percentage(dataframe) == 0


# Empty row/column testing

def test_count_empty_rows_detects_all_null_row():

    # Row 2 empty
    dataframe = pd.DataFrame({
        "name": ["Alice", np.nan],
        "age": [30, np.nan],
    })

    assert count_empty_rows(dataframe) == 1


def test_detect_empty_columns_detects_all_null_column():

    # notes column empty
    dataframe = pd.DataFrame({
        "name": ["Alice", "Bob"],
        "notes": [np.nan, np.nan],
    })

    result = detect_empty_columns(dataframe)

    assert "notes" in result
    assert "name" not in result


# Numeric Summary Testing 

def test_get_numeric_summaries_calculates_correctly():

    dataframe = pd.DataFrame({
        "score": [10, 20, 30, 40],
    })

    result = get_numeric_summaries(dataframe)

    assert result["score"]["min"] == 10.0
    assert result["score"]["max"] == 40.0
    assert result["score"]["mean"] == 25.0
    assert result["score"]["median"] == 25.0


# Quality Score Testing

def test_calculate_column_quality_scores_is_correct():

    # 25% missing, quality score 75%
    dataframe = pd.DataFrame({
        "score": [10, 20, np.nan, 40],
    })

    result = calculate_column_quality_scores(dataframe)

    assert result["score"] == 75.0


def test_calculate_overall_quality_score_applies_duplicate_penalty():

    # 50% duplicate penalty
    dataframe = pd.DataFrame({
        "name": ["Alice", "Alice"],
    })

    assert calculate_overall_quality_score(dataframe) == 50.0


# Quality Score Label Testing

def test_get_quality_score_label_excellent():

    # 90+
    assert get_quality_score_label(90) == "Excellent"
    assert get_quality_score_label(100) == "Excellent"


def test_get_quality_score_label_good():

    # 75 -89
    assert get_quality_score_label(75) == "Good"
    assert get_quality_score_label(89) == "Good"


def test_get_quality_score_label_needs_review():

    # 50 -74
    assert get_quality_score_label(50) == "Needs Review"
    assert get_quality_score_label(74) == "Needs Review"


def test_get_quality_score_label_poor():

    # <50 
    assert get_quality_score_label(49) == "Poor"
    assert get_quality_score_label(0) == "Poor"

def test_get_data_preview_returns_correct_shape():

    # should return first 5 rows with column names and total row count
    dataframe = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "Dan", "Eve", "Frank"],
        "age": [30, 25, 35, 28, 22, 40],
    })

    from quality_check import get_data_preview
    result = get_data_preview(dataframe)

    assert result["preview_count"] == 5          # only first 5 of 6 rows
    assert result["total_rows"] == 6
    assert result["columns"] == ["name", "age"]
    assert result["rows"][0]["name"] == "Alice"


def test_get_data_preview_replaces_nan_with_empty_string():

    import numpy as np
    dataframe = pd.DataFrame({"score": [1.0, np.nan, 3.0]})

    from quality_check import get_data_preview
    result = get_data_preview(dataframe)

    # NaN should become empty string, not "nan"
    assert result["rows"][1]["score"] == ""
