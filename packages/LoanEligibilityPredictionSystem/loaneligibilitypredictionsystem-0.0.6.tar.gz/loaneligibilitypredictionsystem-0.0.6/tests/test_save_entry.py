import pytest
import pandas as pd
from src.preprocessing.preprocessing import preprocess_input

def test_preprocess_valid_data():
    """Test preprocessing with valid input"""
    data = pd.DataFrame({
        'Applicant_Income': [5000],
        'Coapplicant_Income': [2000],
        'Loan_Amount': [300],
        'Loan_Amount_Term': [360],
        'Credit_History': [1],
        'Gender_Male': [1],
        'Married_Yes': [0],
        'Education_Graduate': [1],
        'Self_Employed_Yes': [0],
        'Property_Area': [1]
    })
    result, _ = preprocess_input(data)

    assert result.shape == (1, 10)

def test_preprocess_invalid_data():
    """Test preprocessing with invalid data"""
    with pytest.raises(ValueError):
        preprocess_input(None) 
