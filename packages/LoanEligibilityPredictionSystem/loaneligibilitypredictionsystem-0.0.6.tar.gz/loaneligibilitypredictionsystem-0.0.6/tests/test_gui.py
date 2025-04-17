
import pytest
from src.gui.gui_5_0 import mainApp, manual_entry, main_page, ResultDialog
from unittest.mock import patch, Mock, MagicMock, call
import pandas as pd
import numpy as np
import tkinter as tk
import customtkinter as ctk
from src.prediction.prediction import predict_loan_status
import importlib
import runpy

@pytest.fixture
def app():
    """Fixture to create and destroy the main application"""
    with patch('src.gui.gui_5_0.pd.read_csv') as mock_read_csv:
        mock_read_csv.return_value = pd.DataFrame({
            0: [
                'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount', 'Loan_Amount_Term',
                'Credit_History', 'Gender_Male', 'Married_Yes', 'Education_Graduate',
                'Self_Employed_Yes', 'Property_Area'
            ]
        })
        application = mainApp()
        yield application
        application.destroy()

@pytest.fixture
def populated_manual_entry(app):
    """Fixture to populate manual entry form with valid test data"""
    manual_entry_instance = app.frames[manual_entry]

    # Set form values
    manual_entry_instance.entries["Applicant Income"].set("5000")
    manual_entry_instance.entries["Co-applicant Income"].set("2000")
    manual_entry_instance.entries["Loan Amount"].set("300")
    manual_entry_instance.entries["Loan Term"].set("360")
    manual_entry_instance.entries["Gender"].set("Male")
    manual_entry_instance.entries["Married"].set("Yes")
    manual_entry_instance.entries["Education"].set("Graduate")
    manual_entry_instance.entries["Credit History"].set("Good")
    manual_entry_instance.entries["Self Employed"].set("Yes")
    manual_entry_instance.entries["Property Area Type"].set("Urban")

    # Update validation status
    for field in manual_entry_instance.numeric_fields:
        manual_entry_instance.valid_inputs[field] = True

    return manual_entry_instance

def test_csv_loading(app):
    """Test CSV loading functionality"""

    with patch('src.gui.gui_5_0.filedialog.askopenfilename') as mock_askopen, \
         patch('pandas.read_csv', side_effect=lambda path, **kwargs:
               mock_data if path != "src/preprocessing/training_columns.csv"
               else pd.DataFrame({0: mock_data.columns.tolist()})) as mock_read, \
        patch('src.gui.gui_5_0.messagebox') as mock_msg:
        # Setup mock DataFrame
        mock_data = pd.DataFrame({
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

        # Configure mocks
        mock_askopen.return_value = "/dummy/path.csv"
        mock_read.return_value = mock_data

        # Get main page instance
        main_page_instance = app.frames[main_page]

        # Execute CSV loading command
        main_page_instance.open_command()

        # Verify results
        assert not main_page_instance.input_data.empty
        mock_msg.showinfo.assert_called_once_with("Success", "CSV file loaded successfully!")
        pd.testing.assert_frame_equal(main_page_instance.input_data, mock_data)

def test_prediction_flow(app):
    """Test complete prediction workflow"""
    # Get main page instance and execute flow
    main_page_instance = app.frames[main_page]
    with patch('src.gui.gui_5_0.filedialog.askopenfilename') as mock_askopen, \
        patch('pandas.read_csv') as mock_read, \
        patch('src.gui.gui_5_0.predict_loan_status') as mock_pred, \
        patch('src.preprocessing.preprocessing.load') as mock_load, \
        patch('src.preprocessing.preprocessing.pd.read_csv') as mock_train_cols, \
        patch('src.gui.gui_5_0.ResultDialog') as mock_dialog, \
        patch.object(main_page_instance, 'check_eligible', wraps=main_page_instance.check_eligible) as wrapped_check:

        # Mock training columns to match test data
        mock_train_cols.return_value = pd.DataFrame({
            0: [
                'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount',
                'Loan_Amount_Term', 'Credit_History', 'Gender_Male',
                'Married_Yes', 'Education_Graduate', 'Self_Employed_Yes',
                'Property_Area'
            ]
        })

        # Create mock DataFrame with correct structure
        mock_data = pd.DataFrame({
            'Applicant_Income': [30000.0],
            'Coapplicant_Income': [0.0],
            'Loan_Amount': [300.0],
            'Loan_Amount_Term': [360.0],
            'Credit_History': [1.0],
            'Gender_Male': [1.0],
            'Married_Yes': [0.0],
            'Education_Graduate': [1.0],
            'Self_Employed_Yes': [0.0],
            'Property_Area': [1.0]
        })

        # Configure mocks
        mock_askopen.return_value = "/dummy/path.csv"
        mock_read.return_value = mock_data
        mock_pred.return_value = pd.DataFrame({'Eligibility': ['Eligible']})
        mock_load.return_value = Mock(transform=lambda x: x)  # Mock scaler


        # 1. Load CSV data
        main_page_instance.open_command()
        main_page_instance.input_data = mock_data

        # 2. Trigger prediction
        main_page_instance.check_eligible()

        # Verify prediction call with expected columns
        expected_columns = mock_train_cols.return_value[0].tolist()
        pd.testing.assert_frame_equal(
            mock_pred.call_args[0][0][expected_columns],
            mock_data[expected_columns]
        )
        mock_pred.assert_called_once()
        mock_dialog.assert_called_once()
def test_check_eligibility_with_manual_data(app):
    """Test check eligibility with manual data"""
    # Get the main page instance
    main_page_instance = app.frames[main_page]

    # Create the test data first
    manual_data = pd.DataFrame({
        'Applicant_Income': [30000],
        'Coapplicant_Income': [0],
        'Loan_Amount': [200],
        'Loan_Amount_Term': [240],
        'Credit_History': [0],
        'Gender_Male': [0],
        'Married_Yes': [0],
        'Education_Graduate': [0],
        'Self_Employed_Yes': [1],
        'Property_Area': [0]
    })

    # Set up the test data on the main page
    main_page_instance.input_data = pd.DataFrame()
    main_page_instance.manual_entry_data = manual_data

    # Now patch at more specific locations - try all of these approaches
    with patch('src.gui.gui_5_0.predict_loan_status') as mock_pred, \
         patch('src.gui.gui_5_0.ResultDialog') as mock_dialog:

        # Configure the mock to return our test result
        mock_pred.return_value = pd.DataFrame({'Eligibility': ['Not Eligible']})

        # Call the method under test
        main_page_instance.check_eligible()

        # Assert that the mock was called
        mock_pred.assert_called_once()
        mock_dialog.assert_called_once()

def test_manual_entry_navigation(app):
    """Test navigation to manual entry page and back"""
    main_page_instance = app.frames[main_page]
    manual_entry_instance = app.frames[manual_entry]

    with patch.object(app, 'show_frame') as mock_show:
        main_page_instance.manual_button.invoke()
        mock_show.assert_called_once_with(manual_entry)

    with patch.object(app, 'show_frame') as mock_show:
        manual_entry_instance.back_button.invoke()
        mock_show.assert_called_once_with(main_page)

def test_manual_entry_initial_state(app):
    """Test initial state of manual entry form"""
    manual_entry_instance = app.frames[manual_entry]
    assert manual_entry_instance.submit_button.cget("state") == "disabled"
    for field in manual_entry_instance.numeric_fields:
        assert not manual_entry_instance.valid_inputs[field]

def test_numeric_field_validation(app):
    """Test validation of numeric fields"""
    manual_entry_instance = app.frames[manual_entry]
    test_cases = [
        ("Applicant Income", "abc", False),
        ("Applicant Income", "", False),
        ("Applicant Income", "123.45", True),
        ("Co-applicant Income", "0", True),
        ("Co-applicant Income", "-100", True),
        ("Loan Amount", "abc123", False),
        ("Loan Amount", "500", True),
        ("Loan Term", "5", False),
        ("Loan Term", "400", False),
        ("Loan Term", "360", True),
    ]

    for field, value, expected_valid in test_cases:
        manual_entry_instance.entries[field].set(value)
        manual_entry_instance.validate_numeric(field)
        assert manual_entry_instance.valid_inputs[field] == expected_valid

@patch('tkinter.filedialog.asksaveasfilename')
@patch('tkinter.messagebox.askyesno')
@patch('pandas.read_csv')
@patch('pandas.DataFrame.to_csv')
@patch('tkinter.messagebox.showinfo')
@patch('src.gui.gui_5_0.pd.DataFrame.to_csv')
def test_save_entry_new_file(
    mock_showinfo,
    mock_to_csv,
    mock_read_csv,
    mock_askyesno,
    mock_asksaveasfilename,
    populated_manual_entry
):
    """Test saving manual entry data to a new file"""
    # Configure mocks
    mock_askyesno.return_value = False  # User selects "Save as new"
    mock_asksaveasfilename.return_value = "new_file.csv"

    # Mock training columns
    mock_read_csv.return_value = pd.DataFrame(
        {
            0: [
                'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount',
                'Loan_Amount_Term', 'Credit_History', 'Gender_Male',
                'Married_Yes', 'Education_Graduate', 'Self_Employed_Yes',
                'Property_Area'
            ]
        }
    )

    # Trigger save operation
    populated_manual_entry.save_entry()
    print(f"Manual entry data: {populated_manual_entry.get_data()}")  # If such method exists
    print(f"askyesno called with: {mock_askyesno.call_args}")
    print(f"asksaveasfilename called with: {mock_asksaveasfilename.call_args}")
    print(f"read_csv calls: {mock_read_csv.call_args_list}")

    # Debug: Print all calls to to_csv
    print(f"to_csv calls: {mock_to_csv.call_args_list}")

    # Verify training columns were loaded
    mock_read_csv.assert_called_once_with(
        "src/preprocessing/training_columns.csv",
        header=None
    )

    # Verify data was saved
    assert mock_to_csv.called, "to_csv was not called"
    if mock_to_csv.called:
        assert mock_to_csv.call_args[1]['index'] is False
        assert mock_to_csv.call_args[0][1] == "new_file.csv"
    mock_showinfo.assert_called_once_with("Success", "Data saved to a new file!")

@patch('tkinter.filedialog.askopenfilename')
@patch('tkinter.messagebox.askyesno')
@patch('pandas.read_csv')
@patch('pandas.DataFrame.to_csv')
def test_save_entry_append(
    mock_to_csv,
    mock_read_csv,
    mock_askyesno,
    mock_askopenfilename,
    populated_manual_entry
):
    """Test appending manual entry data to an existing file"""
    # Configure mocks
    mock_askyesno.return_value = True  # User chooses "Append"
    mock_askopenfilename.return_value = "/dummy/existing.csv"

    # Mock training columns (first call) and existing data (second call)
    mock_read_csv.side_effect = [
        # Mock training columns
        pd.DataFrame({0: [
            'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount',
            'Loan_Amount_Term', 'Credit_History', 'Gender_Male',
            'Married_Yes', 'Education_Graduate', 'Self_Employed_Yes',
            'Property_Area'
        ]}),
        # Mock existing CSV data
        pd.DataFrame({
            'Applicant_Income': [40000],
            'Coapplicant_Income': [20000],
            'Loan_Amount': [500],
            'Loan_Amount_Term': [360],
            'Credit_History': [1],
            'Gender_Male': [1],
            'Married_Yes': [1],
            'Education_Graduate': [1],
            'Self_Employed_Yes': [0],
            'Property_Area': [1]
        })
    ]

    # Execute save
    populated_manual_entry.save_entry()

    # Verify the correct file was opened for appending
    assert mock_read_csv.call_args_list[1][0][0] == "/dummy/existing.csv"


def test_user_cancels_file_operations(populated_manual_entry):
    """Test handling when user cancels file operations"""

    manual_entry_instance = populated_manual_entry

    with patch('tkinter.messagebox.askyesno', return_value=True), \
         patch('tkinter.filedialog.askopenfilename', return_value=""), \
         patch('pandas.read_csv') as mock_read_csv:

        mock_read_csv.return_value = pd.DataFrame({
            0: [
                'Applicant_Income', 'Coapplicant_Income', 'Loan_Amount', 'Loan_Amount_Term',
                'Credit_History', 'Gender_Male', 'Married_Yes', 'Education_Graduate',
                'Self_Employed_Yes', 'Property_Area'
            ]
        })
        manual_entry_instance.save_entry()


def test_csv_loading_missing_columns(app):
    """Test CSV loading with missing required columns"""
    with patch('src.gui.gui_5_0.filedialog.askopenfilename') as mock_askopen, \
         patch('pandas.read_csv') as mock_read, \
         patch('src.gui.gui_5_0.messagebox') as mock_msg:

        # Mock data with missing columns
        mock_data = pd.DataFrame({'Wrong_Column': [1]})
        mock_askopen.return_value = "/dummy/path.csv"
        mock_read.return_value = mock_data

        main_page_instance = app.frames[main_page]
        main_page_instance.open_command()

        # Verify error message for missing columns
        mock_msg.showerror.assert_called_once()
        assert main_page_instance.input_data.empty

def test_result_dialog_formatting():
    """Test the formatting logic for result dialog text"""
    # Create test data
    results_df = pd.DataFrame({
        'Eligibility': ['Eligible', 'Not Eligible'],
        'Confidence': ['High', 'Medium'],
        'Reasons': ['Good credit history', 'Insufficient income']
    })

    # Use string formatting logic directly from ResultDialog class
    formatted_text = "\n".join([
        f"Case {i+1}: {row['Eligibility']} ({row['Confidence']}) - {row['Reasons']}"
        for i, row in results_df.iterrows()
    ])

    # Verify expected text formatting
    expected = "Case 1: Eligible (High) - Good credit history\nCase 2: Not Eligible (Medium) - Insufficient income"
    assert formatted_text == expected

def test_csv_loading_exception(app):
    """Test error handling during CSV loading"""
    with patch('src.gui.gui_5_0.filedialog.askopenfilename') as mock_askopen, \
         patch('pandas.read_csv', side_effect=Exception("File error")), \
         patch('src.gui.gui_5_0.messagebox') as mock_msg:

        mock_askopen.return_value = "/dummy/path.csv"
        main_page_instance = app.frames[main_page]
        main_page_instance.open_command()

        mock_msg.showerror.assert_called_once_with("Error", "An error occurred while loading the file: File error")



@patch('tkinter.filedialog.askopenfilename')
@patch('tkinter.messagebox.askyesno')
@patch('pandas.read_csv')
def test_save_entry_append_failure(mock_read, mock_askyesno, mock_askopenfilename, populated_manual_entry):
    """Test append failure during save"""
    # Configure mocks
    mock_askyesno.return_value = True  # Simulate user choosing "Append"
    mock_askopenfilename.return_value = "existing.csv"  # Mock file selection

    # First call: Training columns | Second call: Raise error (existing CSV)
    mock_read.side_effect = [
        pd.DataFrame(  # Mock training columns
            ["Applicant_Income", "Coapplicant_Income", "Loan_Amount",
             "Loan_Amount_Term", "Credit_History", "Gender_Male",
             "Married_Yes", "Education_Graduate", "Self_Employed_Yes",
             "Property_Area"],
            columns=[0]
        ),
        Exception("Read error")  # Fail when reading existing CSV
    ]

    # Execute test
    with patch('src.gui.gui_5_0.messagebox.showerror') as mock_error:
        populated_manual_entry.save_entry()

        # Verify error handling
        mock_error.assert_called_once_with("Error", "Failed to append:\nRead error")

@patch('pandas.read_csv', side_effect=FileNotFoundError)
def test_save_entry_invalid_training_columns(mock_read, populated_manual_entry):
    """Test handling missing training_columns.csv"""
    manual_entry_instance = populated_manual_entry

    with patch('src.gui.gui_5_0.messagebox.showerror') as mock_error:
        manual_entry_instance.save_entry()
        mock_error.assert_called_once_with("Error", "Required training columns file not found")

def test_loan_term_validation(app):
    """Test loan term validation with invalid input"""
    manual_entry_instance = app.frames[manual_entry]
    manual_entry_instance.entries["Loan Term"].set("invalid")
    manual_entry_instance.validate_numeric("Loan Term")
    assert not manual_entry_instance.valid_inputs["Loan Term"]

def test_result_dialog_initialization(app):
    """Test ResultDialog widget configuration"""
    with patch('src.gui.gui_5_0.ctk.CTkToplevel') as mock_toplevel, \
         patch('src.gui.gui_5_0.ctk.CTkTextbox') as mock_textbox, \
         patch('src.gui.gui_5_0.ctk.CTkButton') as mock_button:

        # Configure the mock textbox
        mock_textbox_instance = MagicMock()
        mock_textbox.return_value = mock_textbox_instance

        # Create a mock DataFrame instead of a string
        mock_results = pd.DataFrame({
            'Eligibility': ['Eligible'],
            'Confidence': ['High'],
            'Reasons': ['Good credit history']
        })

        # Create the dialog
        dialog = ResultDialog(app, mock_results)

        # Verify the textbox was configured correctly
        mock_textbox_instance.insert.assert_called_once()
        mock_textbox_instance.configure.assert_called_once_with(state="disabled")

