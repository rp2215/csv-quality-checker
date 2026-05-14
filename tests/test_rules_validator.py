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