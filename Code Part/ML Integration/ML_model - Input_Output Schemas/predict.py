# Contains all the code for making predictions using the trained model

import joblib
import numpy as np
from typing import List

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


# def make_batch_predictions(data_list: List[dict]) -> List[float]:
#     predictions = []
#     for data in data_list:
#         prediction = make_prediction(data)
#         predictions.append(prediction)
#     return predictions


def make_batch_predictions(data_list: List[dict]) -> np.array:
    x = np.array([
        [
            x['latitude'],
            x['housing_median_age'],
            x['total_rooms'],
            x['total_bedrooms'],
            x['population'],
            x['longitude'],
            x['households'],
            x['median_income']
        ]
        for x in data_list
    ])
    return saved_model.predict(x)