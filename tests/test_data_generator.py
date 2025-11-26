import pandas as pd
import pytest
from src.data_generator import generate_data

def test_generate_data_returns_dataframe():
    """
    Tests that generate_data() returns a non-empty pandas DataFrame.
    """
    df = generate_data()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_generate_data_has_expected_columns():
    """
    Tests that the generated DataFrame has the expected columns and dtypes.
    """
    df = generate_data()
    expected_columns = {
        "Category": object,
        "Cause": object,
        "Site": object,
        "Month": object,
        "Year": "int64",
        "Severity": object,
        "Status": object,
        "Count": "int64"
    }

    assert list(df.columns) == list(expected_columns.keys())

    for col, expected_dtype in expected_columns.items():
        assert df[col].dtype == expected_dtype, f"Column {col} has wrong dtype. Expected {expected_dtype}, got {df[col].dtype}"

def test_generate_data_values_are_within_expected_ranges():
    """
    Tests that the values in the generated DataFrame are within the expected ranges.
    """
    df = generate_data()

    # Check that 'Year' is within the expected range
    assert df['Year'].min() >= 2007
    assert df['Year'].max() <= 2009

    # Check that 'Count' is positive
    assert (df['Count'] > 0).all()

    # Check that categorical columns have expected values
    expected_categories = ['Security', 'Equipment', 'Customer', 'Transport', 'Complaint', 'Spill', 'Injury', 'Divergence']
    assert set(df['Category'].unique()).issubset(set(expected_categories))

    expected_severities = ['Critical', 'Major', 'Medium', 'Near Miss']
    assert set(df['Severity'].unique()).issubset(set(expected_severities))

    expected_status = ['Open', 'Closed']
    assert set(df['Status'].unique()).issubset(set(expected_status))