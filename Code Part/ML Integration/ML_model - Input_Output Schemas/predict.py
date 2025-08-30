# Contains all the code for making predictions using the trained model

import joblib
import numpy as np

# Load the trained model from the file
saved_model = joblib.load('model.joblib')
print("Loaded the model from model.joblib")

def make_prediction(data: dict) -> float:
    features = np.array([
        [
            data['longitude'],
            data['latitude'],
            data['housing_median_age'],
            data['total_rooms'],
            data['total_bedrooms'],
            data['population'],
            data['households'],
            data['median_income']
        ]
    ])
    return saved_model.predict(features)[0]

