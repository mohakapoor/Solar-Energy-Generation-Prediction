from weather_api_handler import generate_dataframe_coords
from data_preprocessing import scale_features,zero_nighttime_predictions

import joblib
import numpy as np
import pandas as pd
clat,clon = 28.6139, 77.2090
api_key = "_Your_API_Key"
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
def predict_for_coords(lat,lon):
    

    forecast = generate_dataframe_coords(lat,lon,api_key)
    forecast = scale_features(forecast)
  

    loaded_prophet_model = joblib.load(BASE_DIR / 'solar_energy_project' / 'model_data' / 'prophet_model.joblib')
    predictions = loaded_prophet_model.predict(forecast)


    predictions = zero_nighttime_predictions(forecast,predictions)
    energy = predictions['yhat'] = np.expm1(predictions['yhat'])
    return energy.iloc[0]


print(predict_for_coords(clat,clon))

# def predict_for_coords(lat,lon):
#     api_key = "ec1faaaf4f6046cbdc61fa9da425fbca"

#     forecast = generate_dataframe_coords(lat,lon,api_key)
#     forecast = scale_features(forecast)

#     loaded_prophet_model = joblib.load("solar_energy_project\model_data\\rfr_model.joblib")
#     important_features = ['Solar energy lag1', 'cos_hour', 'Hour', 'Solar energy lag2', 'sin_hour', 'cos_month', 'Cloud coverage', 
#                           'Solar energy lag3', 'Day','Relative humidity', 'Cloud coverage lag1', 'Temperature lag3', 'Temperature', 
#                           'Wind speed', 'Relative humidity lag1', 'Month']
#     X_test = forecast[important_features]
#     predictions = loaded_prophet_model.predict(X_test)


#     # predictions = zero_nighttime_predictions(forecast,predictions)
#     # energy = predictions['yhat'] = np.expm1(predictions['yhat'])
#     energy = np.expm1(predictions[0])
#     return energy.iloc[0]
# print(predict_for_coords(clat,clon))

    

