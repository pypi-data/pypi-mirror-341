import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch
from src.preprocessing.preprocessing import preprocess_input

def test_preprocess_valid_data():
    """Test preprocessing with valid input matching training columns"""
    # Mock the training_columns.csv data
    training_columns = [
        'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount',
        'Loan_Amount_Term', 'Credit_History', 'Gender_Male',
        'Married_Yes', 'Education_Graduate', 'Self_Employed_Yes',
        'Property_Area'
    ]

    # Create valid test data with required columns
    data = pd.DataFrame({
        'Applicant_Income': [5000, 6000, 7000],
        'Coapplicant_Income': [2000, 0, 1000],
        'Loan_Amount': [120, 250, 300],
        'Loan_Amount_Term': [360, 180, 240],
        'Credit_History': [1, 1, 0],
        'Gender_Male': [1, 0, 1],
        'Married_Yes': [1, 0, 1],
        'Education_Graduate': [1, 1, 0],
        'Self_Employed_Yes': [0, 1, 0],
        'Property_Area': [1, 0, 2]  # Encoded as 0=Rural, 1=Semiurban, 2=Urban
    })

    # Mock the training_columns.csv read operation
    with patch('pandas.read_csv') as mock_read:
        mock_read.return_value = pd.DataFrame({0: training_columns})

        # Execute preprocessing
        result, _ = preprocess_input(data)

        # Validate output
        assert result.shape == (3, 10)

def test_preprocess_invalid_data():
    """Test preprocessing with invalid data"""
    with pytest.raises(ValueError) as excinfo:
        preprocess_input(None)
    assert "Input must be a pandas DataFrame" in str(excinfo.value)  # Specific error message
