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
