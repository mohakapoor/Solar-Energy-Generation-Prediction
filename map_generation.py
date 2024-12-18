import folium
from folium import TileLayer
from folium.plugins import HeatMap, MeasureControl
import pandas as pd
import osmnx as ox
import geopandas as gpd
from sklearn.preprocessing import MinMaxScaler
from scipy.interpolate import griddata
import numpy as np
import os
from shapely.geometry import Point
import pandas as pd

def generate_geojson(city):
    delhi_graph = ox.geocoder.geocode_to_gdf(f"{city}, India")
    delhi_graph.to_file(f"{city}_boundary.geojson",driver = "GeoJSON")


# def generate_heat_map(predictions,clat,clon,city):
#     map_center = [clat, clon]
#     delhi_map = folium.Map(location=map_center, zoom_start=12)
#     geojson_file = f"Delhi_boundary.geojson"

#     if geojson_file:
#         folium.GeoJson(geojson_file, name="Delhi Boundary").add_to(delhi_map)

    
#     heat_data = predictions[['Latitude', 'Longitude', 'yhat']].values.tolist()

    
#     HeatMap(heat_data, radius=35,blur=25).add_to(delhi_map)

    
#     delhi_map.save('delhi_heatmap.html')
  
# def generate_heat_map_detail(predictions):
#     min_lat, max_lat = predictions['Latitude'].min(), predictions['Latitude'].max()
#     min_lon, max_lon = predictions['Longitude'].min(), predictions['Longitude'].max()

#     grid_lat, grid_lon = np.meshgrid(np.linspace(min_lat, max_lat,30),  # 
#                                  np.linspace(min_lon, max_lon, 30))
    
#     interpolated_yhat = griddata((predictions['Latitude'], predictions['Longitude']), predictions['yhat'], (grid_lat, grid_lon), method='cubic') 

#     interpolated_yhat = np.nan_to_num(interpolated_yhat, nan=0.0)
#     scaler = MinMaxScaler()
#     scaled_yhat = scaler.fit_transform(interpolated_yhat.flatten().reshape(-1,1))

#     grid_points = pd.DataFrame({
#         'Latitude': grid_lat.flatten(),
#         'Longitude': grid_lon.flatten(),
#         'yhat': scaled_yhat.flatten()
#     })
#     delhi_boundary = gpd.read_file('Delhi_boundary.geojson')
#     delhi_boundary = delhi_boundary.to_crs(epsg=4326) 

#     grid_points['geometry'] = grid_points.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)
#     grid_gdf = gpd.GeoDataFrame(grid_points, geometry='geometry', crs='EPSG:4326')

#     grid_within_delhi = gpd.sjoin(grid_gdf, delhi_boundary, how='inner', predicate='within')

#     heat_data = grid_within_delhi[['Latitude','Longitude','yhat']].values.tolist()

#     map_center = [predictions['Latitude'].mean(), predictions['Longitude'].mean()]
#     delhi_map = folium.Map(location=map_center, zoom_start=12)

#     HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(delhi_map)
    
#     folium.GeoJson(
#         delhi_boundary,
#         name='Delhi Boundary',
#         style_function=lambda x: {'fillColor': 'none', 'color': 'blue', 'weight': 2}
#     ).add_to(delhi_map)

#     # for idx, row in grid_within_delhi.iterrows():
#     #     folium.Marker(
#     #         location=[row['Latitude'], row['Longitude']],
#     #         popup=f"Predicted Value: {row['yhat']:.2f}",
#     #         tooltip=f"Lat: {row['Latitude']:.2f}, Lon: {row['Longitude']:.2f}"
#     #     ).add_to(delhi_map)


#     delhi_map.add_child(MeasureControl(primary_length_unit='kilometers'))
#     delhi_map.save('delhi_heatmap_detail.html')


def generate_heat_map_detail(predictions):
    try:
        if predictions.empty:
            raise ValueError("Predictions dataframe is empty!")

        min_lat, max_lat = predictions['Latitude'].min(), predictions['Latitude'].max()
        min_lon, max_lon = predictions['Longitude'].min(), predictions['Longitude'].max()

        grid_lat, grid_lon = np.meshgrid(np.linspace(min_lat, max_lat, 30),
                                         np.linspace(min_lon, max_lon, 30))

        interpolated_yhat = griddata((predictions['Latitude'], predictions['Longitude']), 
                                     predictions['yhat'], (grid_lat, grid_lon), method='cubic')
        interpolated_yhat = np.nan_to_num(interpolated_yhat, nan=0.0)

        scaler = MinMaxScaler()
        scaled_yhat = scaler.fit_transform(interpolated_yhat.flatten().reshape(-1, 1))

        grid_points = pd.DataFrame({
            'Latitude': grid_lat.flatten(),
            'Longitude': grid_lon.flatten(),
            'yhat': scaled_yhat.flatten()
        })
        print("made the grid")
        if not os.path.exists('Delhi_boundary.geojson'):
            raise FileNotFoundError("Delhi_boundary.geojson not found.")
        delhi_boundary = gpd.read_file('Delhi_boundary.geojson').to_crs(epsg=4326)

        grid_points['geometry'] = grid_points.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)
        grid_gdf = gpd.GeoDataFrame(grid_points, geometry='geometry', crs='EPSG:4326')

        grid_within_delhi = gpd.sjoin(grid_gdf, delhi_boundary, how='inner', predicate='within')
        heat_data = grid_within_delhi[['Latitude', 'Longitude', 'yhat']].values.tolist()

        map_center = [predictions['Latitude'].mean(), predictions['Longitude'].mean()]
        delhi_map = folium.Map(location=map_center, zoom_start=10)
        # MAPBOX_TOKEN = 'pk.eyJ1IjoidGFrdWFuc29obyIsImEiOiJjbTN2eTh5emowc3AzMmxzY3N3Mnp2MHNuIn0.Zgxc2htr6mi3Ix8-cc550Q'  # Replace with your Mapbox token
        # folium.TileLayer(
        #     tiles=f'https://api.mapbox.com/styles/v1/mapbox/dark-v10/tiles/256/{{z}}/{{x}}/{{y}}@2x?access_token={MAPBOX_TOKEN}',
        #     attr='Mapbox',
        #     name='Mapbox Dark',
        #     control=True,
        #     overlay=False
        # ).add_to(delhi_map)

        HeatMap(heat_data, radius=15, blur=10, max_zoom=1).add_to(delhi_map)
        folium.GeoJson(
            delhi_boundary,
            name='Delhi Boundary',
            style_function=lambda x: {'fillColor': 'none', 'color': 'blue', 'weight': 2}
        ).add_to(delhi_map)

        delhi_map.add_child(MeasureControl(primary_length_unit='kilometers'))
        delhi_map.save('delhi_heatmap_detail.html')
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    return delhi_map

def generate_binned_heat_map(predictions, grid_size=50):
    # Get grid boundaries
    min_lat, max_lat = predictions['Latitude'].min(), predictions['Latitude'].max()
    min_lon, max_lon = predictions['Longitude'].min(), predictions['Longitude'].max()

    # Create grid points
    lat_bins = np.linspace(min_lat, max_lat, grid_size)
    lon_bins = np.linspace(min_lon, max_lon, grid_size)

    heat_data = []

    # For each grid cell, calculate the average yhat
    for lat_bin in lat_bins[:-1]:
        for lon_bin in lon_bins[:-1]:
            # Get points within this grid
            mask = (predictions['Latitude'] >= lat_bin) & (predictions['Latitude'] < lat_bins[lat_bins.tolist().index(lat_bin) + 1]) & \
                   (predictions['Longitude'] >= lon_bin) & (predictions['Longitude'] < lon_bins[lon_bins.tolist().index(lon_bin) + 1])

            grid_points = predictions[mask]
            if not grid_points.empty:
                # Calculate the average yhat for this grid cell
                avg_yhat = grid_points['yhat'].mean()
                heat_data.append([lat_bin, lon_bin, avg_yhat])

    # Create the heatmap using the binned data
    map_center = [predictions['Latitude'].mean(), predictions['Longitude'].mean()]
    delhi_map = folium.Map(location=map_center, zoom_start=12)
    HeatMap(heat_data, radius=15, blur=10).add_to(delhi_map)
    delhi_map.save('delhi_heatmap_binned.html')
