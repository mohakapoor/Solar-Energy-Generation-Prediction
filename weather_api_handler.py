import numpy as np
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
import requests
import math 
from datetime import datetime





def generate_dataframe(city,res,radius,api_key):
    def create_city_grid(city, res,radius):
    
        geolocator = Nominatim(user_agent="energy_prediction")
        location = geolocator.geocode(city)
        grid_resolution = [res,res]
        if not location:
            raise ValueError(f"Could not find coordinates for {city}")
        

        def calculate_bounding_box(center_lat, center_lon,radius):
            
            
            north = geodesic(kilometers=radius).destination((center_lat, center_lon), 0)
            south = geodesic(kilometers=radius).destination((center_lat, center_lon), 180)
            east = geodesic(kilometers=radius).destination((center_lat, center_lon), 90)
            west = geodesic(kilometers=radius).destination((center_lat, center_lon), 270)
            
            return {
                'lat_min': south[0],
                'lat_max': north[0],
                'lon_min': west[1],
                'lon_max': east[1]
            }
        
        
        bounds = calculate_bounding_box(location.latitude, location.longitude,radius)
        
        
        lat_range = np.linspace(bounds['lat_min'], bounds['lat_max'], grid_resolution[0])
        lon_range = np.linspace(bounds['lon_min'], bounds['lon_max'], grid_resolution[1])
        
        
        grid_points = []
        for lat in lat_range:
            for lon in lon_range:
                grid_points.append({
                    'Latitude': lat,
                    'Longitude': lon,
                    'Distance_from_center': geodesic(
                        (location.latitude, location.longitude), 
                        (lat, lon)
                    ).kilometers
                })
        grid_df = pd.DataFrame(grid_points,columns=['Latitude','Longitude','Distance_from_center'])
        return grid_df
    try:
        grid_dataframe = create_city_grid(city,res,radius)
    except Exception as e:
        print(f"Error creating grid: {e}")




    def weather_data_genaration(grid_dataframe,api_key):
        weather_data = []
        elevation = 190
        for i in grid_dataframe.index:
            lat = grid_dataframe['Latitude'][i]
            lon = grid_dataframe['Longitude'][i]

            url  = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
            response = requests.get(url)
            weather = response.json()


            temperature_celsius = weather['main']['temp']  
            wind_speed_mps = weather['wind']['speed']  
            relative_humidity = weather['main']['humidity']  
            cloud_coverage = weather['clouds'].get('all',None)
            visibility_meters = weather['visibility']  


            
            a = 17.27
            b = 237.7
            gamma = (a * temperature_celsius) / (b + temperature_celsius) + math.log(relative_humidity / 100)
            dew_point = (b * gamma) / (a - gamma)

            visibility_miles = visibility_meters / 1609.34
            wind_speed_mph = wind_speed_mps * 2.23694 

            station_pressure = weather["main"].get("pressure")
            sea_level = weather["main"].get("sea_level")

            station_pressure_inchHg = station_pressure*0.02953

            altimeter = sea_level*(1-elevation/44330)**(-5.255)
            altimeter_inchHg = altimeter*0.02953


            weather_data.append({
                'ds' : datetime(2018,10,29,hour=12,minute=0),
                'Timezone' : 'Asia/Kolkata',
                'Cloud coverage' : cloud_coverage,
                'Visibility' : visibility_miles,
                'Temperature': temperature_celsius,
                'Dew point': dew_point,
                'Relative humidity' : relative_humidity,
                'Wind speed' : wind_speed_mph,
                'Station pressure' : station_pressure_inchHg,
                'Altimeter' : altimeter_inchHg


            })
        weather_data = pd.DataFrame(weather_data,columns=['ds','Cloud coverage','Visibility','Temperature','Dew point','Relative humidity','Wind speed','Station pressure','Altimeter','Timezone'])
        
        return weather_data

    weather_data = weather_data_genaration(grid_dataframe,api_key)
    forecast = pd.merge(grid_dataframe,weather_data,left_index=True,right_index=True)
    return forecast


def generate_dataframe_coords(lat,lon,api_key):
    weather_data = []
    elevation = 190
    url  = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    response = requests.get(url)
    weather = response.json()

    temperature_celsius = weather['main']['temp']  
    wind_speed_mps = weather['wind']['speed']  
    relative_humidity = weather['main']['humidity']  
    cloud_coverage = weather['clouds'].get('all',None)
    visibility_meters = weather['visibility']  


    
    a = 17.27
    b = 237.7
    gamma = (a * temperature_celsius) / (b + temperature_celsius) + math.log(relative_humidity / 100)
    dew_point = (b * gamma) / (a - gamma)

    visibility_miles = visibility_meters / 1609.34
    wind_speed_mph = wind_speed_mps * 2.23694 

    station_pressure = weather["main"].get("pressure")
    sea_level = weather["main"].get("sea_level")

    station_pressure_inchHg = station_pressure*0.02953

    altimeter = sea_level*(1-elevation/44330)**(-5.255)
    altimeter_inchHg = altimeter*0.02953

    spec_date = datetime(2018, 10, 29, hour=datetime.now().hour, minute=0)
    weather_data.append({
        'ds' : spec_date,
        'Timezone' : 'Asia/Kolkata',
        'Latitude' : lat,
        'Longitude' : lon,
        'Cloud coverage' : cloud_coverage,
        'Visibility' : visibility_miles,
        'Temperature': temperature_celsius,
        'Dew point': dew_point,
        'Relative humidity' : relative_humidity,
        'Wind speed' : wind_speed_mph,
        'Station pressure' : station_pressure_inchHg,
        'Altimeter' : altimeter_inchHg,
        'Solar energy lag1': 126.78,
        'Solar energy lag2': 338.5,
        'Solar energy lag3': 728.5,
        'Cloud coverage lag1': 1,
        'Visibility lag1': 10,
        'Temperature lag1': 3.77,
        'Dew point lag1': 0,
        'Relative humidity lag1': 75.64,
        'Wind speed lag1': 8.28,
        'Station pressure lag1': 29.16,
        'Altimeter lag1': 29.95,
        'Cloud coverage lag2': 1,
        'Visibility lag2': 10,
        'Temperature lag2': 4.18,
        'Dew point lag2': -0.04,
        'Relative humidity lag2': 74.6,
        'Wind speed lag2': 12.16,
        'Station pressure lag2': 29.14,
        'Altimeter lag2': 29.93,
        'Cloud coverage lag3': 1,
        'Visibility lag3': 10,
        'Temperature lag3': 4.72,
        'Dew point lag3': -0.5,
        'Relative humidity lag3': 69.04,
        'Wind speed lag3': 12.76,
        'Station pressure lag3': 29.14,
        'Altimeter lag3': 29.93,
        'Hour' : spec_date.hour,
        'Month' : spec_date.month,
        'Day' : spec_date.day,
        'sin_hour' : np.sin(2 * np.pi *spec_date.hour / 24),
        'cos_hour' : np.cos(2 * np.pi *spec_date.hour / 24),
        'sin_month' : np.sin(2 * np.pi * spec_date.month / 12),
        'cos_month' : np.cos(2 * np.pi * spec_date.month / 12)})
    weather_data = pd.DataFrame(weather_data,columns=[
    'ds', 'Timezone', 'Latitude', 'Longitude', 'Cloud coverage', 'Visibility', 
    'Temperature', 'Dew point', 'Relative humidity', 'Wind speed', 'Station pressure', 
    'Altimeter', 'Solar energy lag1', 'Solar energy lag2', 'Solar energy lag3', 
    'Cloud coverage lag1', 'Visibility lag1', 'Temperature lag1', 'Dew point lag1', 
    'Relative humidity lag1', 'Wind speed lag1', 'Station pressure lag1', 
    'Altimeter lag1', 'Cloud coverage lag2', 'Visibility lag2', 'Temperature lag2', 
    'Dew point lag2', 'Relative humidity lag2', 'Wind speed lag2', 'Station pressure lag2', 
    'Altimeter lag2', 'Cloud coverage lag3', 'Visibility lag3', 'Temperature lag3', 
    'Dew point lag3', 'Relative humidity lag3', 'Wind speed lag3', 'Station pressure lag3', 
    'Altimeter lag3', 'Hour', 'Month', 'Day','sin_hour', 'cos_hour', 'sin_month', 'cos_month'
    ])

  

    return weather_data


