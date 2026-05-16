import pytest

from batch_processor import find_csv_files, process_single_csv, process_csv_folder

# Find CSV File Testing

def test_find_csv_files_raises_error_for_missing_folder():

    # folder doesnt exist should return FileNotFoundError
    with pytest.raises(FileNotFoundError):
        find_csv_files("/nonexistent/folder")


def test_find_csv_files_raises_error_when_path_is_a_file(tmp_path):

    # using with file instead of folder should return ValueError
    file = tmp_path / "test.csv"
    file.write_text("name\nAlice\n")

    with pytest.raises(ValueError):
        find_csv_files(file)


def test_find_csv_files_raises_error_when_no_csvs_found(tmp_path):

    # empty folder should return FileNotFoundError
    with pytest.raises(FileNotFoundError):
        find_csv_files(tmp_path)


def test_find_csv_files_returns_csv_files_in_folder(tmp_path):

    # create 2 CSV files in folder and should find both
    (tmp_path / "a.csv").write_text("name\nAlice\n")
    (tmp_path / "b.csv").write_text("name\nBob\n")

    result = find_csv_files(tmp_path)

    assert len(result) == 2


def test_find_csv_files_ignores_non_csv_files(tmp_path):

    # .txt file should be ignored
    (tmp_path / "data.csv").write_text("name\nAlice\n")
    (tmp_path / "notes.txt").write_text("some notes")

    result = find_csv_files(tmp_path)

    assert len(result) == 1


def test_find_csv_files_recursive_finds_files_in_subfolders(tmp_path):

    # should only find CSV file in subfolder when recursive set to True
    subfolder = tmp_path / "sub"
    subfolder.mkdir()
    (subfolder / "nested.csv").write_text("name\nAlice\n")

    # no CSV files in top folder
    with pytest.raises(FileNotFoundError):
        find_csv_files(tmp_path, recursive=False)

    # finds sub folders with recursive
    result = find_csv_files(tmp_path, recursive=True)
    assert len(result) == 1


# Process Single CSV Tests

def test_process_single_csv_returns_success_for_valid_file(tmp_path):

    # valid CSV file
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25\n")

    result = process_single_csv(csv_file)

    assert result["status"] == "success"
    assert result["results"] is not None
    assert result["error"] is None


def test_process_single_csv_returns_failed_for_invalid_file(tmp_path):

    # non existsnet should be returned as failed result not raising exception
    result = process_single_csv("/nonexistent/file.csv")

    assert result["status"] == "failed"
    assert result["error"] is not None


def test_process_single_csv_includes_rules_validation_when_rules_provided(tmp_path):

    # rules passed should return a rules_validation section
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age\nAlice,30\n")

    rules = {"columns": {"name": {"required": True}}}

    result = process_single_csv(csv_file, rules=rules)

    assert result["status"] == "success"
    assert result["results"]["rules_validation"] is not None


def test_process_single_csv_rules_validation_is_none_when_no_rules(tmp_path):

    # no rules passed shouldnt return rules_validation section
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age\nAlice,30\n")

    result = process_single_csv(csv_file)

    assert result["results"]["rules_validation"] is None


# Process CSV Folder Tests

def test_process_csv_folder_returns_results_for_all_files(tmp_path):

    # valid files
    (tmp_path / "a.csv").write_text("name\nAlice\n")
    (tmp_path / "b.csv").write_text("name\nBob\n")

    results = process_csv_folder(tmp_path)

    assert len(results) == 2


def test_process_csv_folder_continues_after_failed_file(tmp_path):

    # process shouldnt stop when one file fails
    (tmp_path / "valid.csv").write_text("name\nAlice\n")
    (tmp_path / "empty.csv").write_text("")  # empty file will fail load_csv

    results = process_csv_folder(tmp_path)

    statuses = [r["status"] for r in results]

    assert "success" in statuses
    assert "failed" in statuses
