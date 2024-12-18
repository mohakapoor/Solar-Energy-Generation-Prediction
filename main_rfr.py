from weather_api_handler import generate_dataframe_coords
from data_preprocessing import scale_features,zero_nighttime_predictions_rfr

import joblib
import numpy as np
import pandas as pd
clat,clon = 28.6139, 77.2090

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

def predict_for_coords_rfr(lat,lon):
    api_key = "_Your_API_Key"

    forecast = generate_dataframe_coords(lat,lon,api_key)
    forecast = scale_features(forecast)
    important_features = ['Solar energy lag1', 'cos_hour', 'Hour', 'Solar energy lag2', 'sin_hour', 'cos_month', 'Cloud coverage', 'Solar energy lag3', 'Day', 'Relative humidity', 'Cloud coverage lag1', 'Temperature lag3', 'Temperature', 'Wind speed', 'Relative humidity lag1', 'Month']

    loaded_prophet_model = joblib.load(BASE_DIR / 'solar_energy_project' / 'model_data' / 'rfr_model.joblib')
    
    predictions = loaded_prophet_model.predict(forecast[important_features])
    predictions = zero_nighttime_predictions_rfr(forecast,predictions)
    energy = predictions = np.expm1(predictions)
    return energy[0]

