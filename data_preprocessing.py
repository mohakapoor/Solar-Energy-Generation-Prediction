import joblib
from sklearn.preprocessing import MinMaxScaler,StandardScaler
from astral import LocationInfo
from astral.sun import sun
import pytz
from pathlib import Path
import numpy as np

def scale_features(forecast):
    BASE_DIR = Path(__file__).resolve().parent.parent
    loaded_minmax_scaler = joblib.load(BASE_DIR / 'solar_energy_project' / 'model_data' / 'min_max_scaler.joblib')
    loaded_standard_scaler = joblib.load(BASE_DIR / 'solar_energy_project' / 'model_data' / 'standard_scaler.joblib')

    min_max_features = ['Cloud coverage','Visibility','Relative humidity', 'Cloud coverage lag1','Cloud coverage lag2','Cloud coverage lag3',
                        'Visibility lag1','Visibility lag2','Visibility lag3','Relative humidity lag1','Relative humidity lag2',
                        'Relative humidity lag3']
    standard_features = ['Temperature','Dew point','Wind speed','Station pressure','Altimeter','Temperature lag1','Temperature lag2','Temperature lag3','Dew point lag1',
                        'Dew point lag2','Dew point lag3','Wind speed lag1','Wind speed lag2','Wind speed lag3','Station pressure lag1','Station pressure lag2',
                        'Station pressure lag3','Altimeter lag1','Altimeter lag2','Altimeter lag3']
    lagged_solar_features = ['Solar energy lag1','Solar energy lag2','Solar energy lag3']

    forecast[min_max_features] = loaded_minmax_scaler.transform(forecast[min_max_features])
    forecast[standard_features] = loaded_standard_scaler.transform(forecast[standard_features])
    forecast[lagged_solar_features] = np.log1p(forecast[lagged_solar_features])
    
    return forecast




def zero_nighttime_predictions(forecast,predictions):
    def is_daylight(ts, timezone, latitude, longitude):
        location_tz = pytz.timezone(timezone)
        location = LocationInfo(
            name="Your Location",
            region="Region",
            timezone=timezone,
            latitude=latitude,
            longitude=longitude
        )
        s = sun(location.observer, date=ts.date())
        sunrise = s['sunrise'].astimezone(location_tz)
        sunset = s['sunset'].astimezone(location_tz)
        
        # Make 'ts' timezone-aware by localizing it
        ts = ts.replace(tzinfo=location_tz) if ts.tzinfo is None else ts.astimezone(location_tz)
        
        return sunrise <= ts <= sunset
        
    for i in forecast.index:
        ts = forecast['ds'][i]  
        timezone = 'Asia/Kolkata'
        latitude = forecast['Latitude'][i]
        longitude = forecast['Longitude'][i]
        # print(f"datetime = {ts}, daytime = {is_daylight(ts,timezone,latitude,longitude)}")
 
        if not is_daylight(ts, timezone, latitude, longitude):
            predictions.at[i, 'yhat'] = 0  
        
    predictions['yhat'] = predictions['yhat'].clip(lower =0)
    return predictions


def zero_nighttime_predictions_rfr(forecast,predictions):
    def is_daylight(ts, timezone, latitude, longitude):
        location_tz = pytz.timezone(timezone)
        location = LocationInfo(
            name="Your Location",
            region="Region",
            timezone=timezone,
            latitude=latitude,
            longitude=longitude
        )
        s = sun(location.observer, date=ts.date())
        sunrise = s['sunrise'].astimezone(location_tz)
        sunset = s['sunset'].astimezone(location_tz)
        
        # Make 'ts' timezone-aware by localizing it
        ts = ts.replace(tzinfo=location_tz) if ts.tzinfo is None else ts.astimezone(location_tz)
        
        return sunrise <= ts <= sunset
        
    for i in forecast.index:
        ts = forecast['ds'][i]  
        timezone = 'Asia/Kolkata'
        latitude = forecast['Latitude'][i]
        longitude = forecast['Longitude'][i]
        # print(f"datetime = {ts}, daytime = {is_daylight(ts,timezone,latitude,longitude)}")
 
        if not is_daylight(ts, timezone, latitude, longitude):
            predictions.at[i] = 0  
        
    predictions = np.clip(predictions,a_min=0,a_max=None)
    return predictions

