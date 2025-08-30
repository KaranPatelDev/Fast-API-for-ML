# Contains all logic for all api endpoints
from fastapi import FastAPI
from schemas import InputSchema, OutputSchema
from predict import make_prediction, make_batch_predictions
from typing import List
import pandas as pd  # Add this import at the top

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Welcome to the ML Prediction API"}

@app.post("/prediction", response_model=OutputSchema)
def predict(user_input: InputSchema):
    prediction = make_prediction(user_input.model_dump())
    # Convert to Python float to avoid JSON serialization issues
    prediction_value = float(prediction) if hasattr(prediction, 'item') else float(prediction)
    # Fix field name to match OutputSchema - should be 'prediction' not 'predicted_price'
    return OutputSchema(prediction=round(prediction_value, 2))




@app.post("/predict_batch", response_model=List[OutputSchema])
def predict_batch(user_inputs: List[InputSchema]):
    # Use the same logic as single prediction for each item in the batch
    predictions = []
    for user_input in user_inputs:
        prediction = make_prediction(user_input.model_dump())
        prediction_value = float(prediction) if hasattr(prediction, 'item') else float(prediction)
        predictions.append(OutputSchema(prediction=round(prediction_value, 2)))
    return predictions




'''
Example JSON input for testing the /prediction endpoint:
[
  {
    "longitude": -122.05,
    "latitude": 37.42,
    "housing_median_age": 30,
    "total_rooms": 1200,
    "total_bedrooms": 500,
    "population": 1000,
    "households": 450,
    "median_income": 5.65
  },
  {
    "longitude": -118.32,
    "latitude": 34.05,
    "housing_median_age": 18,
    "total_rooms": 2200,
    "total_bedrooms": 850,
    "population": 1600,
    "households": 700,
    "median_income": 8.12
  },
  {
    "longitude": -121.75,
    "latitude": 38.55,
    "housing_median_age": 45,
    "total_rooms": 650,
    "total_bedrooms": 300,
    "population": 500,
    "households": 200,
    "median_income": 4.33
  },
  {
    "longitude": -119.78,
    "latitude": 36.74,
    "housing_median_age": 28,
    "total_rooms": 1800,
    "total_bedrooms": 600,
    "population": 1300,
    "households": 550,
    "median_income": 6.75
  },
  {
    "longitude": -117.16,
    "latitude": 32.72,
    "housing_median_age": 22,
    "total_rooms": 3000,
    "total_bedrooms": 1100,
    "population": 2500,
    "households": 900,
    "median_income": 9.05
  }
]

'''