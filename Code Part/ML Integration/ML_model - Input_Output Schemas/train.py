# Contains all logic for training the model

import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the dataset
df = pd.read_csv('housing.csv').iloc[:, :-1].dropna()

# Split the data into features and target variable
X = df.drop(columns=['median_house_value'])
Y = df.median_house_value.copy()
print("Split the dataset")

# Train the model
model = LinearRegression().fit(X, Y)
print("Trained the model")

# Save the trained model to a file
joblib.dump(model, 'model.joblib')
print("Saved the model to model.joblib")
