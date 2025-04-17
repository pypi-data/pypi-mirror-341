import pandas as pd
import numpy as np
import tensorflow as tf
from keras.api.models import Sequential
from keras.api.layers import Dense, Dropout, BatchNormalization
from keras.api.optimizers import Adam
from keras.api.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
from joblib import dump

def encode_property_area(data):
    """Encodes Property_Area_Semiurban and Property_Area_Urban into a single column."""
    data["Property_Area"] = 0  # Default to Rural (0)
    data.loc[data["Property_Area_Semiurban"] == 1, "Property_Area"] = 1  # Semiurban (1)
    data.loc[data["Property_Area_Urban"] == 1, "Property_Area"] = 2  # Urban (2)

    # Drop the original one-hot columns
    data.drop(columns=["Property_Area_Semiurban", "Property_Area_Urban"], errors="ignore", inplace=True)
    
    return data

# basic data preprocessing, can be better oop and put into a differnt file if needed
data = pd.read_csv("src/model/dataset.csv")
data = data.drop(columns=["Loan_ID"])  # drop the Loan_ID column, not needed for training

data = pd.get_dummies(data, drop_first=True) # one-hot encode categorical variables, drop_first=True to avoid dummy variable trap

data = encode_property_area(data)

data = data.dropna() # drop rows with missing values, can be better to fill with mean or median
#print(data.columns)
data.rename(columns={"Education_Not Graduate": "Education_Graduate", "ApplicantIncome": "Applicant_Income", "CoapplicantIncome":"Coapplicant_Income", "LoanAmount" : "Loan_Amount"}, inplace=True)
data = data.drop(["Dependents_1","Dependents_2","Dependents_3+"], axis=1)
pd.Series(data.columns).to_csv("src/preprocessing/training_columns.csv", index=False, header=False)

#print(data.head())
#print(data.shape)   

y = data["Loan_Status_Y"].astype(int) 
X = data.drop(columns=["Loan_Status_Y"]) # drop the target variable
pd.Series(X.columns).to_csv("src/preprocessing/training_columns.csv", index=False, header=False)

scaler = StandardScaler() # standardize the data, mean = 0, std = 1, might use MinMaxScaler() instead
# scaler = MinMaxScaler() # scale the data to a range, might use StandardScaler() instead
X = scaler.fit_transform(X)

from joblib import dump
dump(scaler, "src/preprocessing/scaler.joblib")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # 80% training, 20% testing can be changed

#print(y_train.value_counts())
#print(y_test.value_counts())

# SMOTE to fix data imbalance
smote = SMOTE(sampling_strategy='auto', random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

print("New Class Distribution:", np.bincount(y_train_resampled))

# random forest to see if it can do better and for feature importance
rf_model = RandomForestClassifier()
rf_model.fit(X_train_resampled, y_train_resampled)

feature_importances = pd.Series(rf_model.feature_importances_, index=data.drop(columns=["Loan_Status_Y"]).columns)
print(feature_importances.sort_values(ascending=False))

rf_y_pred = rf_model.predict(X_test)
rf_accuracy = accuracy_score(y_test, rf_y_pred)
print(f"Random Forest Test Accuracy: {rf_accuracy * 100:.2f}%")

# deep neural network
model = Sequential([
    # input layer
    Dense(1024, activation='relu', input_shape=(X_train.shape[1],)), # 256 is the number of neurons, can be changed
    # hidden layers
    BatchNormalization(), # normalizes the input layer
    Dropout(0.6), # dropout rate, can be changed

    Dense(256, activation='relu', input_shape=(X_train.shape[1],)),
    BatchNormalization(),
    Dropout(0.4),

    Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    BatchNormalization(),
    Dropout(0.3),

    Dense(64, activation='relu'),
    BatchNormalization(),
    Dropout(0.4),

    Dense(32, activation='relu'),
    BatchNormalization(),
    Dropout(0.2),

    Dense(1, activation='sigmoid')  # binary classification
])

# compile
model.compile(optimizer=Adam(learning_rate=0.01), # learning rate is .001, can be changed
              loss='binary_crossentropy',
              metrics=['accuracy'])

# train
model.summary()

early_stop = EarlyStopping(monitor='val_loss', patience=200, restore_best_weights=True)

history = model.fit(X_train_resampled, y_train_resampled, epochs=500, batch_size=16, # hyperparameters, epochs = 50, batch_size = 32, can be changed
                    validation_data=(X_test, y_test), callbacks=[early_stop], 
                    verbose=2) # hyperparameters, epochs = 50, batch_size = 32, can be changed

# evalutate
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy * 100:.2f}%")

#model.save("src/model/lenn1.3.keras")

# plot accuracy and loss
train_acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
train_loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(train_acc) + 1)

# plot accuracy
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(epochs, train_acc, 'b-', label='Training Accuracy')
plt.plot(epochs, val_acc, 'r-', label='Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('Training & Validation Accuracy')
plt.legend()

# plot loss
plt.subplot(1, 2, 2)
plt.plot(epochs, train_loss, 'b-', label='Training Loss')
plt.plot(epochs, val_loss, 'r-', label='Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('Training & Validation Loss')
plt.legend()

plt.show()

# notes 1.0
# need data set to work with
# testing flexibility of scrum approach with the delay of the model implementation
# basic implementation of a model
# haven't begun to train or test
# haven't begun to perfect hyper parameters

# notes 1.1
# struggled importing the data set and preprocessing
# used get_dummies to one-hot encode categorical variables
# renamed some of the dataframe columns, had to change the refrence in the y variable
# model is trained and tested
# accuracy is 65%
# need to test with more data, more epochs, and/or more hyperparameters
# the *fun* part is just beginning, tweaking the model to get better results. trial and error.
# save model to h5 file
# import h5 file for predictions
# we will need to create a new file for predictions for predictions and data preprocessing, 
# as the model data set and all incoming data points will need to be preprocessed the same way

# notes 1.2
# val accuracy is stuck at 65%
# checked for data imbalance, found imbalance
# trying to fix data imbalance with Class Weights and SMOTE
# SMOTE worked, but class weights didn't
# val acccuracy jumps to 81.13% with loss still dropping
# Trying to use random forest to see if it can do better and for feature importance

# notes 1.3
# generating model 1.2 for better predictions
# added more layers and neurons
# tweaked dropout
# adding a graph showing accuracy and loss
# implemented early stopping, very useful

# notes 1.4
# data preprocessing on area so now it is 0 = rural, 1 = semiurban, 2 = urban
