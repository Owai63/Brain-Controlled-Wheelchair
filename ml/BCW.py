import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Directory containing CSV files
directory = '/content/drive/MyDrive/Dataset/'

# Iterate over files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        # Load the dataset
        file_path = os.path.join(directory, filename)
        data = pd.read_csv(file_path)

        # Correct column names by stripping leading/trailing spaces
        data.columns = data.columns.str.strip()

        # Prepare the data
        X = data.drop(['class', 'obs', 'time'], axis=1)  # Exclude non-feature columns
        y = data['class']

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Standardize the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train a Support Vector Machine (SVM) model
        svm_model = SVC(kernel='rbf', random_state=42)
        svm_model.fit(X_train_scaled, y_train)

        # Make predictions on the test set
        y_pred = svm_model.predict(X_test_scaled)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        classification_rep = classification_report(y_test, y_pred)

        print(f'File: {filename}')
        print(f'Accuracy: {accuracy}')
        print('Classification Report:')
        print(classification_rep)
        print('\n')

