import pytest
import numpy as np
from src.prediction.prediction import predict_loan_status
from src.preprocessing.preprocessing import preprocess_input
from unittest.mock import patch

def test_model_prediction(trained_model):
    """Test model prediction shape and range"""
    dummy_input = np.random.rand(1, 10)
    prediction = trained_model.predict(dummy_input)
    assert prediction.shape == (1, 1)
    assert 0 <= prediction[0][0] <= 1

def test_prediction_format(sample_csv_data):
    """Test prediction service output format"""
    with patch('src.preprocessing.preprocessing.preprocess_input') as mock_preprocess:
        mock_preprocess.return_value = (np.array([[0.5]*10]), [0])
        results = predict_loan_status(sample_csv_data)
        assert not results.empty
        assert 'Eligibility' in results.columns
        assert results.shape[0] == 1

def test_batch_prediction(trained_model, large_csv_data):
    """Test batch prediction capabilities"""
    processed, _ = preprocess_input(large_csv_data)
    predictions = trained_model.predict(processed)
    assert predictions.shape == (1000, 1)
    assert (predictions >= 0).all() and (predictions <= 1).all()
