#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json
import pandas as pd
import geopandas as gpd
import streamlit as st
import leafmap

# Set the app configuration
st.set_page_config(layout="wide", page_title="Transit Guides", page_icon=":bus:")

# Set the title of the Streamlit app
st.title("Transit General Urban Information and Destination Explorer (TransitGUIDE) Prototype")

# Add the description text below the title
st.markdown("""
This prototype includes a single transit system and a handful of destinations.
Select a destination category to identify the locations of businesses within 1/4 mile of a WMATA station.
Click on the circle to see the name of the business.
""")

# Load the stations CSV file into a DataFrame
stations_df = pd.read_csv('df1.csv')

# Load the pre-fetched data from the JSON file
with open('pre_fetched_data.json', 'r') as f:
    pre_fetched_data = json.load(f)

# Create a GeoDataFrame for stations
stations_gdf = gpd.GeoDataFrame(
    stations_df,
    geometry=gpd.points_from_xy(stations_df['stations_lo'], stations_df['stations_la'])
)

# Extract coordinates and names from the GeoDataFrame
station_coords = list(zip(stations_gdf.geometry.y, stations_gdf.geometry.x, stations_gdf['station_name']))

# Define the process_amenities function
def process_amenities(amenities_data):
    results = []
    if 'elements' in amenities_data:
        for element in amenities_data['elements']:
            name = element['tags'].get('name', 'Unnamed Location')  # Default to 'Unnamed Location'
            if 'lat' in element and 'lon' in element:
                results.append({
                    'name': name,
                    'lat': element['lat'],
                    'lon': element['lon']
                })
            elif 'center' in element:
                results.append({
                    'name': name,
                    'lat': element['center']['lat'],
                    'lon': element['center']['lon']
                })
    return results

# Create the map using leafmap
def create_leaflet_map(station_coords, amenities=None):
    # Initialize the map centered on downtown DC
    m = leafmap.Map(center=[38.89511, -77.03637], zoom=12, control_scale=True)

    # Add station markers to the map
    for lat, lon, station_name in station_coords:
        if lat is not None and lon is not None:
            print(f"Adding station: {station_name}, Location: {lat}, {lon}")  # Debugging line
            m.add_marker(location=[lat, lon], popup=station_name)
        else:
            print(f"Invalid coordinates for station: {station_name}")  # Debugging line

    if amenities:
        # Define colors for different amenities
        color_map = {
            'hotel': 'blue',
            'cafe': 'green',
            'childcare': 'orange',
            'pizza': 'purple',
            'cinema': 'yellow',
            'library': 'brown',
            'supermarket': 'red'
        }

        for amenity_name, amenity_info in amenities.items():
            for amenity in amenity_info:
                if amenity['lat'] is not None and amenity['lon'] is not None:
                    print(f"Adding amenity: {amenity['name']}, Location: {amenity['lat']}, {amenity['lon']}")  # Debugging line
                    m.add_marker(location=[amenity['lat'], amenity['lon']], popup=amenity['name'], icon_color=color_map.get(amenity_name, 'gray'))
                else:
                    print(f"Invalid coordinates for amenity: {amenity['name']}")  # Debugging line

    return m

# Streamlit Dropdown
destination = st.selectbox(
    'Select your destination:',
    ['Select your destination', 'hotel', 'cafe', 'childcare', 'pizza', 'cinema', 'library', 'supermarket']
)

# Create the map based on the selected destination
if destination != 'Select your destination':
    amenities_data = {}
    for station_name, station_data in pre_fetched_data.items():
        processed_data = process_amenities(station_data[destination])
        if processed_data:
            if destination not in amenities_data:
                amenities_data[destination] = []
            amenities_data[destination].extend(processed_data)

    # Create the map with amenities
    map_object = create_leaflet_map(station_coords, amenities=amenities_data)
else:
    map_object = create_leaflet_map(station_coords)

# Display the map
map_object.to_streamlit(width=1200, height=1000)

