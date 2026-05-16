import pytest
import pandas as pd

from csv_loader import load_csv, find_duplicate_column_names

# tmp_path creates a temp directory for each test cleaning it after test complte

# File Loading Tests

def test_load_csv_returns_dataframe_for_valid_file(tmp_path):

    # create csv file in temp directory
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25\n")

    result = load_csv(csv_file)

    # should return df with correct shape
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2, 2)


def test_load_csv_stores_duplicate_column_names_in_attrs(tmp_path):

    # should store name in attrs as it is present twice
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age,name\nAlice,30,Smith\n")

    result = load_csv(csv_file)

    assert "name" in result.attrs["duplicate_column_names"]


def test_load_csv_has_no_duplicate_column_names_when_all_unique(tmp_path):

    # attrs list should be empty as all names are unique
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age,email\nAlice,30,a@b.com\n")

    result = load_csv(csv_file)

    assert result.attrs["duplicate_column_names"] == []

def test_load_csv_raises_error_for_missing_file():

    # Passing a path that doesn't exist should raise FileNotFoundError
    with pytest.raises(FileNotFoundError):
        load_csv("/nonexistent/path/file.csv")


def test_load_csv_raises_error_for_non_csv_file(tmp_path):

    # .txt file should be rejected
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("name,age\nAlice,30\n")

    with pytest.raises(ValueError):
        load_csv(txt_file)


def test_load_csv_raises_error_for_empty_file(tmp_path):

    # empty CSV file should be rejected
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")

    with pytest.raises(ValueError):
        load_csv(empty_file)

# Duplicate Column Name Testing

def test_find_duplicate_column_names_detects_duplicates(tmp_path):

    # "score" present twice
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,score,score\nAlice,10,20\n")

    result = find_duplicate_column_names(csv_file)

    assert "score" in result


def test_find_duplicate_column_names_returns_empty_for_unique_headers(tmp_path):

    # all unique result should be empty
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age,score\nAlice,30,95\n")

    result = find_duplicate_column_names(csv_file)

    assert result == []
