import pandas as pd

from rules_validator import validate_dataframe_all_rules


def test_required_column_exists_passes():

    dataframe = pd.DataFrame(
        {
            "age": [21, 32, 45],
        }
    )

    rules = {
        "columns": {
            "age": {
                "required": True,
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    assert result["overall_passed"] is True
    assert result["columns"]["age"]["passed"] is True


def test_required_column_missing_fails():

    dataframe = pd.DataFrame(
        {
            "name": ["Alice", "Bob"],
        }
    )

    rules = {
        "columns": {
            "age": {
                "required": True,
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    assert result["overall_passed"] is False
    assert result["columns"]["age"]["passed"] is False


def test_allowed_values_fails_for_unexpected_value():

    dataframe = pd.DataFrame(
        {
            "status": ["Active", "Inactive", "Unknown"],
        }
    )

    rules = {
        "columns": {
            "status": {
                "required": True,
                "allowed_values": [
                    "Active",
                    "Inactive",
                ],
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    assert result["overall_passed"] is False
    assert result["columns"]["status"]["passed"] is False

def test_type_number_passes_for_valid_values():

    # mix of integers and decimals both valid
    dataframe = pd.DataFrame(
        {
            "score": [1, 2.5, 100, 0.99],
        }
    )

    rules = {
        "columns": {
            "score": {
                "required": True,
                "type": "number",
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    assert result["overall_passed"] is True
    assert result["columns"]["score"]["passed"] is True

def test_type_number_fails_for_invalid_values():

    # "abc" value should trigger failure
    dataframe = pd.DataFrame(
        {
            "score": [1,2,"abc"],
        }
    )
    
    rules = {
        "columns": {
            "score": {
                "required": True,
                "type": "number",
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe,rules)

    # invalid value column and overall should fail
    assert result["overall_passed"] is False
    assert result["columns"]["score"]["passed"] is False

def test_type_text_always_passes():

    # all CSV values are strings so should never fail
    dataframe = pd.DataFrame(
        {
            "name": ["Alice", "Bob", "Charlie"],
        }
    )

    rules = {
        "columns": {
            "name": {
                "required": True,
                "type": "text",
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    assert result["overall_passed"] is True
    assert result["columns"]["name"]["passed"] is True

def test_type_text_passes_with_mixed_content():

    dataframe = pd.DataFrame(
        {
            "notes": ["hello", "123", "true", "3.14"],
        }
    )

    rules = {
        "columns": {
            "notes": {
                "required": True,
                "type": "text",
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    # text type should always pass
    assert result["overall_passed"] is True
    assert result["columns"]["notes"]["passed"] is True


# Check Pattern Tests

def test_pattern_passes_when_all_values_match():

    # all names letters and spaces only
    dataframe = pd.DataFrame({
        "name": ["Alice Smith", "Bob Jones", "Charlie"],
    })

    rules = {
        "columns": {
            "name": {
                "required": True,
                "pattern": "^[A-Za-z ]+$",
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    assert result["overall_passed"] is True
    assert result["columns"]["name"]["passed"] is True


def test_pattern_fails_when_values_dont_match():

    # letters only pattern should reject "Alice123"
    dataframe = pd.DataFrame({
        "name": ["Alice", "Bob", "Alice123"],
    })

    rules = {
        "columns": {
            "name": {
                "required": True,
                "pattern": "^[A-Za-z ]+$",
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    assert result["overall_passed"] is False
    assert result["columns"]["name"]["passed"] is False


def test_pattern_ignores_missing_values():

    # NaN values should be skipped
    dataframe = pd.DataFrame({
        "name": ["Alice", None, "Bob"],
    })

    rules = {
        "columns": {
            "name": {
                "required": True,
                "pattern": "^[A-Za-z ]+$",
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    # "NaN value should not cause failure
    assert result["overall_passed"] is True
    assert result["columns"]["name"]["passed"] is True


def test_pattern_fails_for_invalid_regex():

    dataframe = pd.DataFrame({
        "name": ["Alice", "Bob"],
    })

    rules = {
        "columns": {
            "name": {
                "required": True,
                "pattern": "[invalid(",  # invalid regex
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    # should return failure not a crash
    assert result["overall_passed"] is False
    assert result["columns"]["name"]["passed"] is False


def test_pattern_validates_email_format():

    # validate an email column against an email regex
    dataframe = pd.DataFrame({
        "email": ["alice@example.com", "bob@test.org", "not-an-email"],
    })

    rules = {
        "columns": {
            "email": {
                "required": True,
                "pattern": r"^[\w.+-]+@[\w-]+\.[\w.]+$",
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    # "not-an-email" doesn't match — should fail
    assert result["overall_passed"] is False
    assert result["columns"]["email"]["passed"] is False

# Unique Rule Tests

def test_unique_passes_when_all_values_are_unique():

    # all IDs are different — should pass
    dataframe = pd.DataFrame({"id": [1, 2, 3, 4]})

    rules = {"columns": {"id": {"required": True, "unique": True}}}

    result = validate_dataframe_all_rules(dataframe, rules)

    assert result["overall_passed"] is True
    assert result["columns"]["id"]["passed"] is True


def test_unique_fails_when_duplicates_exist():

    # value 1 appears twice — should fail
    dataframe = pd.DataFrame({"id": [1, 2, 1, 3]})

    rules = {"columns": {"id": {"required": True, "unique": True}}}

    result = validate_dataframe_all_rules(dataframe, rules)

    assert result["overall_passed"] is False
    assert result["columns"]["id"]["passed"] is False


def test_unique_ignores_missing_values():

    # two NaN values should not count as duplicates of each other
    dataframe = pd.DataFrame({"id": [1, None, 2, None]})

    rules = {"columns": {"id": {"required": True, "unique": True}}}

    result = validate_dataframe_all_rules(dataframe, rules)

    # remaining values 1 and 2 are unique — should pass
    assert result["overall_passed"] is True
    assert result["columns"]["id"]["passed"] is True


def test_unique_skipped_when_rule_set_to_false():

    # unique: false means the check is disabled entirely
    dataframe = pd.DataFrame({"id": [1, 1, 1]})

    rules = {"columns": {"id": {"required": True, "unique": False}}}

    result = validate_dataframe_all_rules(dataframe, rules)

    # duplicates ignored because rule is off — should pass
    assert result["overall_passed"] is True
    assert result["columns"]["id"]["passed"] is True


# Date Range Tests

def test_date_range_passes_when_all_dates_in_range():

    # all dates fall within 2024
    dataframe = pd.DataFrame({
        "signup_date": ["2024-01-01", "2024-06-15", "2024-12-31"]
    })

    rules = {
        "columns": {
            "signup_date": {
                "required": True,
                "date_min": "2024-01-01",
                "date_max": "2024-12-31",
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    assert result["overall_passed"] is True
    assert result["columns"]["signup_date"]["passed"] is True


def test_date_range_fails_when_date_before_min():

    # 2023-12-31 is before the 2024-01-01 lower bound
    dataframe = pd.DataFrame({
        "signup_date": ["2023-12-31", "2024-06-15"]
    })

    rules = {
        "columns": {
            "signup_date": {"required": True, "date_min": "2024-01-01"}
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    assert result["overall_passed"] is False
    assert result["columns"]["signup_date"]["passed"] is False


def test_date_range_fails_when_date_after_max():

    # 2025-01-01 is after the 2024-12-31 upper bound
    dataframe = pd.DataFrame({
        "signup_date": ["2024-06-15", "2025-01-01"]
    })

    rules = {
        "columns": {
            "signup_date": {"required": True, "date_max": "2024-12-31"}
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    assert result["overall_passed"] is False
    assert result["columns"]["signup_date"]["passed"] is False


def test_date_range_fails_for_non_date_values():

    # "not-a-date" cannot be parsed — check should fail clearly rather than crash
    dataframe = pd.DataFrame({
        "signup_date": ["2024-01-01", "not-a-date"]
    })

    rules = {
        "columns": {
            "signup_date": {
                "required": True,
                "date_min": "2024-01-01",
                "date_max": "2024-12-31",
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    assert result["overall_passed"] is False
    assert result["columns"]["signup_date"]["passed"] is False


def test_date_range_ignores_missing_values():

    # None should be skipped — only the two present dates are checked
    dataframe = pd.DataFrame({
        "signup_date": ["2024-06-01", None, "2024-09-15"]
    })

    rules = {
        "columns": {
            "signup_date": {
                "required": True,
                "date_min": "2024-01-01",
                "date_max": "2024-12-31",
            }
        }
    }

    result = validate_dataframe_all_rules(dataframe, rules)

    # both present dates are valid — should pass
    assert result["overall_passed"] is True
    assert result["columns"]["signup_date"]["passed"] is True
