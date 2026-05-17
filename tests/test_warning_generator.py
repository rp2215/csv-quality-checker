from warning_generator import (
    create_empty_warnings,
    check_missing_values_warnings,
    check_duplicate_row_warnings,
    check_empty_row_warnings,
    check_empty_column_warnings,
    check_duplicate_column_name_warnings,
    check_overall_quality_warnings,
    has_warnings,
    generate_warnings,
)

# Missing Value Tests

def test_missing_values_100_percent_is_critical():

    # 100% missing
    results = {"missing_percentage": {"score": 100}}
    warnings = create_empty_warnings()
    check_missing_values_warnings(results, warnings)

    assert len(warnings["CRITICAL"]) == 1


def test_missing_values_above_50_percent_is_high():

    # 75% missing
    results = {"missing_percentage": {"score": 75}}
    warnings = create_empty_warnings()
    check_missing_values_warnings(results, warnings)

    assert len(warnings["HIGH"]) == 1


def test_missing_values_above_25_percent_is_medium():

    # 30% missing 
    results = {"missing_percentage": {"score": 30}}
    warnings = create_empty_warnings()
    check_missing_values_warnings(results, warnings)

    assert len(warnings["MEDIUM"]) == 1


def test_missing_values_above_10_percent_is_low():

    # 15% missing 
    results = {"missing_percentage": {"score": 15}}
    warnings = create_empty_warnings()
    check_missing_values_warnings(results, warnings)

    assert len(warnings["LOW"]) == 1


def test_missing_values_at_or_below_10_percent_has_no_warning():

    # 5% missing no warning
    results = {"missing_percentage": {"score": 5}}
    warnings = create_empty_warnings()
    check_missing_values_warnings(results, warnings)

    assert not has_warnings(warnings)

# Duplicate Row Tests

def test_duplicate_rows_generates_medium_warning():

    # any duplicate rows should return medium
    results = {"duplicate_rows": 2, "duplicate_percentage": 50.0}
    warnings = create_empty_warnings()
    check_duplicate_row_warnings(results, warnings)

    assert len(warnings["MEDIUM"]) == 1


def test_no_duplicate_rows_has_no_warning():

    # No duplicates should return no warning
    results = {"duplicate_rows": 0, "duplicate_percentage": 0}
    warnings = create_empty_warnings()
    check_duplicate_row_warnings(results, warnings)

    assert not has_warnings(warnings)

# Empty Row Tests

def test_empty_rows_generates_medium_warning():

    # if any completly empty rows return medium
    results = {"empty_rows": 1}
    warnings = create_empty_warnings()
    check_empty_row_warnings(results, warnings)

    assert len(warnings["MEDIUM"]) == 1


def test_no_empty_rows_has_no_warning():

    # none empty should return no warning
    results = {"empty_rows": 0}
    warnings = create_empty_warnings()
    check_empty_row_warnings(results, warnings)

    assert not has_warnings(warnings)

# Empty Column Tests

def test_empty_column_generates_critical_warning():

    # no values in column should return critical
    results = {"empty_columns": ["notes"]}
    warnings = create_empty_warnings()
    check_empty_column_warnings(results, warnings)

    assert len(warnings["CRITICAL"]) == 1


def test_no_empty_columns_has_no_warning():

    # non empty should return no warning
    results = {"empty_columns": []}
    warnings = create_empty_warnings()
    check_empty_column_warnings(results, warnings)

    assert not has_warnings(warnings)

# Duplicate Column Name Tests

def test_duplicate_column_name_generates_high_warning():

    # has duplicate name should return high
    results = {"duplicate_column_names": ["name"]}
    warnings = create_empty_warnings()
    check_duplicate_column_name_warnings(results, warnings)

    assert len(warnings["HIGH"]) == 1


def test_no_duplicate_column_names_has_no_warning():

    # no duplicate name should return no warning
    results = {"duplicate_column_names": []}
    warnings = create_empty_warnings()
    check_duplicate_column_name_warnings(results, warnings)

    assert not has_warnings(warnings)

# Overall Quality Score Tests

def test_overall_quality_below_25_is_critical():

    results = {"overall_quality_score": 20}
    warnings = create_empty_warnings()
    check_overall_quality_warnings(results, warnings)

    assert len(warnings["CRITICAL"]) == 1


def test_overall_quality_below_50_is_high():

    results = {"overall_quality_score": 40}
    warnings = create_empty_warnings()
    check_overall_quality_warnings(results, warnings)

    assert len(warnings["HIGH"]) == 1


def test_overall_quality_below_75_is_medium():

    results = {"overall_quality_score": 60}
    warnings = create_empty_warnings()
    check_overall_quality_warnings(results, warnings)

    assert len(warnings["MEDIUM"]) == 1


def test_overall_quality_at_or_above_75_has_no_warning():

    # 75 or above should return no warning
    results = {"overall_quality_score": 75}
    warnings = create_empty_warnings()
    check_overall_quality_warnings(results, warnings)

    assert not has_warnings(warnings)

def test_generate_warnings_returns_warnings_for_bad_data():

    # should produce multiple warnings
    results = {
        "missing_percentage": {"score": 100},   # CRITICAL
        "duplicate_rows": 3,
        "duplicate_percentage": 30.0,            # MEDIUM
        "empty_rows": 0,
        "empty_columns": [],
        "duplicate_column_names": [],
        "unique_values": {},
        "missing_values": {},
        "row_count": 10,
        "overall_quality_score": 20,             # CRITICAL
    }

    warnings = generate_warnings(results)

    # at least 1 critical warning should be returned
    assert len(warnings["CRITICAL"]) >= 1

def test_custom_thresholds_change_warning_severity():

    # default 30% missing is medium 
    # if threshold raised to 40% defualt should no longer be active
    results = {"missing_percentage": {"score": 30}}
    warnings = create_empty_warnings()

    # supply a custom threshold that raises the MEDIUM bar above 30%
    custom_thresholds = {
        **__import__("warning_generator").DEFAULT_THRESHOLDS,
        "missing_medium": 40,   # only trigger MEDIUM if above 40%, not the default 25%
    }

    check_missing_values_warnings(results, warnings, thresholds=custom_thresholds)

    # 30% is below the new MEDIUM threshold of 40 — should produce no MEDIUM warning
    assert len(warnings["MEDIUM"]) == 0
