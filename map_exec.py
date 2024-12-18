from weather_api_handler import generate_dataframe
from data_preprocessing import scale_features,zero_nighttime_predictions
from map_generation import generate_heat_map_detail,generate_geojson,generate_binned_heat_map
import joblib
import numpy as np
import pandas as pd



api_key = "ec1faaaf4f6046cbdc61fa9da425fbca"
api_key_2 = "2da24311dd44cdc6e2c76650184f57ca"

clat,clon = 28.6139, 77.2090

# forecast = generate_dataframe('New Delhi',20,35,api_key)
# joblib.dump(forecast,'forecast_day.pkl')

forecast = joblib.load('solar_energy_project\\forecast_day.pkl')
print(forecast.columns)
print(forecast)


forecast = scale_features(forecast)
# print(forecast)


loaded_prophet_model = joblib.load("model_data\prophet_model.joblib")
predictions = loaded_prophet_model.predict(forecast)

predictions = zero_nighttime_predictions(forecast,predictions)
# print(predictions['yhat'])

predictions['yhat'] = np.expm1(predictions['yhat'])
# print(predictions['yhat'])
# print(predictions['yhat'].min())

spatial_predictions = forecast.copy()
spatial_predictions['yhat'] = predictions['yhat']
print(spatial_predictions['yhat'])
# generate_geojson("Delhi")

print(generate_heat_map_detail(spatial_predictions))
