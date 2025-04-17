import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, mock_open, patch
from keras.models import load_model
from faker import Faker
from sklearn.preprocessing import StandardScaler

fake = Faker()

# Add mock preprocessing artifacts
@pytest.fixture(autouse=True)
def mock_preprocessing_files():
    with patch("pandas.read_csv") as mock_csv:
        # Mock training columns to match test data structure
        mock_csv.side_effect = lambda path, **kw: pd.DataFrame({0: [
            'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount',
            'Loan_Amount_Term', 'Credit_History', 'Gender_Male',
            'Married_Yes', 'Education_Graduate', 'Self_Employed_Yes',
            'Property_Area'
        ]}) if "training_columns" in path else pd.read_csv(path, **kw)

    with patch("joblib.load") as mock_load:
        # Mock scaler with identity transformation
        mock_scaler = StandardScaler()
        mock_scaler.mean_ = np.zeros(10)
        mock_scaler.scale_ = np.ones(10)
        mock_load.return_value = mock_scaler
        yield


@pytest.fixture
def sample_csv_data():
    return pd.DataFrame({
        'Applicant_Income': [30000],
        'Coapplicant_Income': [0],
        'Loan_Amount': [300],
        'Loan_Amount_Term': [360],
        'Credit_History': [1],
        'Gender_Male': [1],
        'Married_Yes': [0],
        'Education_Graduate': [1],
        'Self_Employed_Yes': [0],
        'Property_Area': [1]
    })

@pytest.fixture
def sample_raw_data():
    return pd.DataFrame({
        'Gender': ['Male'],
        'Married': ['No'],
        'Education': ['Graduate'],
        'Self_Employed': ['No'],
        'ApplicantIncome': [30000],
        'CoapplicantIncome': [0],
        'LoanAmount': [300],
        'Loan_Amount_Term': [360],
        'Credit_History': [1.0],
        'Property_Area': ['Semiurban']
    })

@pytest.fixture(scope="module")
def trained_model():
    return load_model("src/model/lenn1.3.keras")

@pytest.fixture
def large_csv_data():
    """Batch of 1000 samples with edge cases"""
    np.random.seed(42)
    size = 1000

    data = pd.DataFrame({
        'Applicant_Income': np.random.randint(1000, 100000, size),
        'Coapplicant_Income': np.random.randint(0, 50000, size),
        'Loan_Amount': np.random.randint(10, 1000, size),
        'Loan_Amount_Term': np.random.choice([12, 36, 60, 120, 240, 360], size),
        'Credit_History': np.random.randint(0, 2, size),
        'Gender_Male': np.random.randint(0, 2, size),
        'Married_Yes': np.random.randint(0, 2, size),
        'Education_Graduate': np.random.randint(0, 2, size),
        'Self_Employed_Yes': np.random.randint(0, 2, size),
        'Property_Area': np.random.randint(0, 3, size)
    })

    data.iloc[0] = [0, 0, 0, 0, -1, 2, 2, 2, 2, 4]
    data.iloc[1:10] = np.nan
    data.iloc[10:20, 0] = 1e6
    return data

@pytest.fixture
def large_raw_data():
    """Batch of 1000 raw samples with realistic fake data"""
    size = 1000
    data = pd.DataFrame({
        'Gender': np.random.choice(['Male', 'Female', 'Other'], size),
        'Married': np.random.choice(['Yes', 'No'], size),
        'Education': np.random.choice(['Graduate', 'Not Graduate'], size),
        'Self_Employed': np.random.choice(['Yes', 'No'], size),
        'ApplicantIncome': np.abs(np.random.normal(15000, 10000, size)).astype(int),
        'CoapplicantIncome': np.abs(np.random.normal(5000, 3000, size)).astype(int),
        'LoanAmount': np.random.randint(9, 700, size),
        'Loan_Amount_Term': np.random.choice([12, 36, 60, 120, 240, 360], size),
        'Credit_History': np.random.choice([0, 1, np.nan], size),
        'Property_Area': np.random.choice(['Urban', 'Semiurban', 'Rural'], size)
    })

    data['Gender'] = data['Gender'].apply(lambda x: fake.random_element(
        elements=('Male', 'Female', 'M', 'F', 'male', 'female')))
    return data

@pytest.fixture
def mixed_type_data():
    """Data with type inconsistencies"""
    return pd.DataFrame({
        'Applicant_Income': ['30k', 'forty thousand', 'N/A'],
        'Coapplicant_Income': [0, 'none', ''],
        'Loan_Amount': [300.5, 'three hundred', None],
        'Loan_Amount_Term': ['360 months', 240, 180.5],
        'Credit_History': ['Yes', 'No', 1],
        'Gender_Male': [True, 'M', 2],
        'Married_Yes': ['Y', 1, 0],
        'Education_Graduate': ['Grad', 1, '0'],
        'Self_Employed_Yes': [np.nan, 'Yes', 'No'],
        'Property_Area': [1, 'Urban', 3]
    })

@pytest.fixture
def malformed_csv_data():
    """Data with structural issues"""
    return pd.DataFrame({
        'Unrelated_Column1': [1, 2, 3],
        'Bad_Column2': ['a', 'b', 'c'],
        'Loan_ID': ['LP001', 'LP002', 'LP003']
    })
