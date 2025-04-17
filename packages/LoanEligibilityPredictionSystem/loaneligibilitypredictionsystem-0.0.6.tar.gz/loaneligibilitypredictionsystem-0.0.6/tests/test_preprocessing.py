import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, Mock
from src.preprocessing.preprocessing import preprocess_input

@pytest.fixture
def sample_raw_data():
    """Fixture providing data in the format after GUI manual entry preprocessing."""
    return pd.DataFrame({
        'Applicant_Income': [5000],
        'Coapplicant_Income': [2000],
        'Loan_Amount': [300],
        'Loan_Amount_Term': [360],
        'Credit_History': [1],
        'Gender_Male': [1],
        'Married_Yes': [0],
        'Education_Graduate': [1],
        'Self_Employed_Yes': [0],
        'Property_Area': [1]  # Encoded as 0=Rural, 1=Semiurban, 2=Urban
    })

def test_preprocessing(sample_raw_data):
    """Test standard preprocessing workflow with GUI-formatted data."""
    with patch('pandas.read_csv') as mock_cols, \
         patch('joblib.load') as mock_scaler:

        mock_cols.return_value = pd.Series([
            'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount',
            'Loan_Amount_Term', 'Credit_History', 'Gender_Male',
            'Married_Yes', 'Education_Graduate', 'Self_Employed_Yes',
            'Property_Area'
        ])
        mock_scaler.return_value = Mock(transform=lambda x: x)

        processed, _ = preprocess_input(sample_raw_data)
        assert processed.shape == (1, 10)
        assert 'Property_Area' in sample_raw_data.columns

def test_missing_columns():
    invalid_data = pd.DataFrame({'Loan_ID': ['LP001'], 'Wrong_Column': [1]})

    with pytest.raises(ValueError) as excinfo:
        preprocess_input(invalid_data)
    assert "Missing required columns" in str(excinfo.value)

def test_batch_preprocessing(large_csv_data):
    processed, _ = preprocess_input(large_csv_data)
    assert processed.shape == (1000, 10)
    assert np.isfinite(processed).all()

def test_mixed_type_handling(mixed_type_data):
    with pytest.raises(ValueError) as excinfo:
        preprocess_input(mixed_type_data)
    assert "Invalid numeric value" in str(excinfo.value)
