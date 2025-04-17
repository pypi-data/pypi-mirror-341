# Add this at the top of your src/gui/gui_5_0.py
import os
import sys

# Set DLL search path to help find NumPy dependencies
if hasattr(os, 'add_dll_directory'):  # Windows specific
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        # Add the lib/numpy/core directory to the DLL search path
        numpy_core_path = os.path.join(application_path, 'lib', 'numpy', 'core')
        if os.path.exists(numpy_core_path):
            os.add_dll_directory(numpy_core_path)
        # Also add the main executable directory for MKL DLLs
        os.add_dll_directory(application_path)

# Now try to import NumPy
try:
    import numpy
except ImportError as e:
    import traceback
    # Create an error log if numpy fails to import
    with open('numpy_error.log', 'w') as f:
        f.write(f"Error importing NumPy: {e}\n")
        f.write(traceback.format_exc())
        f.write("\nPython path: " + str(sys.path))
        f.write("\nExecutable path: " + sys.executable)
        if hasattr(os, 'environ'):
            f.write("\nPATH: " + os.environ.get('PATH', 'N/A'))
    # Re-raise to show the error
    raise

import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
try:
    # For frozen executable
    from src.preprocessing.preprocessing import preprocess_input
    from src.prediction.prediction import predict_loan_status
except ImportError:
    # For development environment
    from preprocessing.preprocessing import preprocess_input
    from prediction.prediction import predict_loan_status

# Configure CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class mainApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        '''Initialize the main UI class to serve as container for all pages.'''

        super().__init__(*args, **kwargs)
        self.title("Loan Eligibility Application")
        self.geometry("380x600")

        # Configure the main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Initialize frames vairable to an empty array
        self.frames = {}

        #Define a tuple of unique page classes and iteratively configure each page
        for F in (main_page, manual_entry):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        #Display the main page first
        self.show_frame(main_page)

    def show_frame(self, cont):
        '''Display additional pages when passed page titles as parameters'''

        frame = self.frames[cont]
        frame.tkraise()


class main_page(ctk.CTkFrame):
    '''Class definition for main UI page and associated buttons'''

    def __init__(self, parent, controller):
        '''Initializes the main page'''

        #Frame initialization call
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # Define widgets
        label = ctk.CTkLabel(self, text="Loan Eligibility Checker",
                           font=("Arial", 20, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=20)

        self.load_button = ctk.CTkButton(self, text="Load CSV File", command=self.open_command)
        self.load_button.grid(row=1, column=0, padx=10, pady=10)

        self.manual_button = ctk.CTkButton(self, text="Manual Data Entry",
                                         command=lambda: controller.show_frame(manual_entry))
        self.manual_button.grid(row=1, column=1, padx=10, pady=10)

        self.submit_button = ctk.CTkButton(self, text="Check Eligibility", command=self.check_eligible)
        self.submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=20)

        # Initialize data storage
        self.input_data = pd.DataFrame()
        self.manual_entry_data = pd.DataFrame()

    def open_command(self):
        '''Generates tkinter file dialog and loads a selected .CSV file to a pandas DataFrame'''

        try:
            path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not path:  # If user cancels file selection
                return
            data = pd.read_csv(path)
            #Print the columns and first few rows of the data
            print("\n\nActual CSV Columns:\n", data.columns.tolist())
            
            #Dropping the loan_Id column if it exists
            if "Loan_ID" in data.columns:
                data.drop(columns=["Loan_ID"], inplace=True)

            data.columns = data.columns.str.strip().str.replace(" ", "_").str.title()
            training_cols_path = os.path.join(os.path.dirname(__file__), '../preprocessing/training_columns.csv')
            required_columns = pd.read_csv(training_cols_path, header=None).squeeze("columns").tolist()


            print("\n \nModified CSV Columns:\n", data.columns.tolist())
            missing_cols = [col for col in required_columns if col not in data.columns]

            #Check for missing columns
            if missing_cols:
                print(required_columns)
                print(data.columns)
                messagebox.showerror("Error", f"Missing columns in CSV: {', '.join(missing_cols)}")
                return

            #Select only relevant columns
            self.input_data = data[required_columns]

            self.data = data
            print(self.data)

            messagebox.showinfo("Success", "CSV file loaded successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the file: {e}")

   # In main_page class
    def check_eligible(self):
        if not self.input_data.empty:
           prediction = predict_loan_status(self.input_data)  # Should use the CSV data
           ResultDialog(self.master, prediction)
        elif not self.manual_entry_data.empty:
           prediction = predict_loan_status(self.manual_entry_data)
           ResultDialog(self.master, prediction)
        else:
           messagebox.showwarning("No Data", "Load CSV or enter manual data first")

class manual_entry(ctk.CTkFrame):
    '''Class definition for manual data entry page and associated fields and buttons'''

    def __init__(self, parent, controller):
        '''Initializes the page'''

        
        #Frame initialization call
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        #Define labels
        label = ctk.CTkLabel(self, text="Manual Entry Page",
                           font=("Arial", 20, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=20)

        #Define entry fields
        self.entries = {}
        fields = [
            ("Gender", "gender"),
            ("Married", "option"),
            ("Education", "education"),
            ("Self Employed", "option" ),
            ("Applicant Income", "number"),
            ("Co-applicant Income", "number"),
            ("Loan Amount", "number"),
            ("Loan Term", "number"),
            ("Credit History", "credit"),
            ("Property Area Type", "area")
        ]

        for row, (label_text, field_type) in enumerate(fields, 1):
            ctk.CTkLabel(self, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            var = ctk.StringVar()

            if field_type == "gender":
                entry = ctk.CTkOptionMenu(self, variable=var, values=["X", "Female", "Male"])
            elif field_type == "option":
                entry = ctk.CTkOptionMenu(self, variable=var, values=["Yes", "No"])
            elif field_type == "education":
                entry = ctk.CTkOptionMenu(self, variable=var, values=["Graduate", "Not Graduate"])
            elif field_type == "credit":
                entry = ctk.CTkOptionMenu(self, variable=var, values=["Bad", "Good"])
            elif field_type == "area":
                entry = ctk.CTkOptionMenu(self, variable=var, values=["Urban", "Semiurban", "Rural"])
            else:
                entry = ctk.CTkEntry(self, textvariable=var)

            entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            self.entries[label_text] = var

        #Validate numeric fields
        self.numeric_fields = [
            "Applicant Income",
            "Co-applicant Income",
            "Loan Amount",
            "Loan Term",
        ]

        #Track validation state
        self.valid_inputs = {field: False for field in self.numeric_fields}

        #Attach validations
        for field in self.numeric_fields:
            self.entries[field].trace_add("write", lambda name, index, mode, f=field: self.validate_numeric(f))

        #Define buttons
        self.back_button = ctk.CTkButton(self, text="Back to Main",
                     command=lambda: controller.show_frame(main_page))
        self.back_button.grid(row=12, column=0, padx=10, pady=20)

        self.submit_button = ctk.CTkButton(self, text="Submit Entry", command=self.save_entry,
                                           state="disabled")
        self.submit_button.grid(row=12, column=1, padx=10, pady=20)

    def validate_numeric(self, field):
        '''Ensures numeric fields contain valid inputs'''
        value = self.entries[field].get().strip()

        #Validate non-empty fields
        valid = False
        if value:
            try:
                float(value)
                valid = True
            except ValueError:
               valid = False
        if field == "Loan Term":
            try:
                term = float(value)
                valid = (term >= 12) and (term <= 360) #Validate values expressed in months
            except:
                valid = False

        self.valid_inputs[field] = valid
        all_valid = all(self.valid_inputs.values())

        #Debug outputs
        print(f"Field '{field}': {value} | Valid: {valid}")
        print(f"All valid: {all_valid}")

        self.submit_button.configure(state="normal" if all_valid else "disabled")

    def save_entry(self):
        '''Collects user input and saves it into pandas DataFrame'''

        data = {
        # Numeric fields (convert strings to numbers)
        "Applicant_Income": float(self.entries["Applicant Income"].get()),
        "Coapplicant_Income": float(self.entries["Co-applicant Income"].get()),
        "Loan_Amount": float(self.entries["Loan Amount"].get()),
        "Loan_Amount_Term": float(self.entries["Loan Term"].get()),

        # Binary-encoded categoricals
        "Gender_Male": 1 if self.entries["Gender"].get() == "Male" else 0,
        "Married_Yes": 1 if self.entries["Married"].get() == "Yes" else 0,
        "Education_Graduate": 1 if self.entries["Education"].get() == "Graduate" else 0,
        "Credit_History": 1 if self.entries["Credit History"].get() == "Good" else 0,
        "Self_Employed_Yes": 1 if self.entries["Self Employed"].get() == "Yes" else 0,

        # Property Area encoding (0=Rural, 1=Semiurban, 2=Urban)
        "Property_Area": {
            "Rural": 0,
            "Semiurban": 1,
            "Urban": 2
        }[self.entries["Property Area Type"].get()]
        }

        #Convert input to DataFrame
        self.manual_entry_data = pd.DataFrame([data])

        #Match entry column order to training columns
        try:
            training_cols_path = os.path.join(os.path.dirname(__file__), '../preprocessing/training_columns.csv')
            training_cols = pd.read_csv(training_cols_path, header=None)[0].tolist()
            self.manual_entry_data = self.manual_entry_data[training_cols]

            #Ask user to save as new or append to existing
            append = messagebox.askyesno("Save Options", "Append to existing CSV file?\n(Click 'No' to save as a new file)")

            if append:
                # APPEND TO EXISTING FILE FLOW
                path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
                if not path:  # User cancellation
                    return

                try:
                    existing_data = pd.read_csv(path)
                    combined_data = pd.concat([existing_data, self.manual_entry_data], ignore_index=True)
                    combined_data.to_csv(path, index=False)  # overwrite selected file
                    messagebox.showinfo("Success", "Data appended to existing file!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to append:\n{e}")
            else:
                # SAVE AS NEW FILE FLOW
                path = filedialog.asksaveasfilename(
                    defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv")],
                    title="Save as new CSV"
                )
                if not path:  # User cancellation
                    return

                try:
                    self.manual_entry_data.to_csv(path, index=False)
                    messagebox.showinfo("Success", "Data saved to a new file!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save:\n{e}")

        except FileNotFoundError:
            messagebox.showerror("Error", "Required training columns file not found")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read training columns:\n{e}")
            return

class ResultDialog(ctk.CTkToplevel):
    """Custom resizable dialog for displaying eligibility results."""
    def __init__(self, parent, results_df):
        super().__init__(parent)
        self.title("Eligibility Result")
        self.geometry("600x400")  # Set default size (width x height)

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Add scrollable text box
        self.textbox = ctk.CTkTextbox(self, wrap="none")
        self.textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.textbox.insert("1.0",
            "\n".join([f"Case {i+1}: {row['Eligibility']} "
                      f"({row['Confidence']}) - {row['Reasons']}"
                      for i, row in results_df.iterrows()]))
        self.textbox.configure(state="disabled")  # Make it read-only

        # Close button
        self.button = ctk.CTkButton(self, text="Close", command=self.destroy)
        self.button.grid(row=1, column=0, pady=10)

if __name__ == '__main__':
    app = mainApp()
    app.mainloop()
