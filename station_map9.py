#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import folium
from folium import CircleMarker, Circle
import pandas as pd
from streamlit_folium import st_folium

# Read the .csv file into a DataFrame
gdf = pd.read_csv('CTA.csv')  # Update the file path as needed

# Function to plot the map
def plot_map(desired_station_name, gdf):
    # Check if 'station_name' column exists
    if 'station_name' not in gdf.columns:
        st.error("Station name column not found in the data.")
        return None

    # Filter the data by station name
    filtered_gdf = gdf[gdf['station_name'].str.lower() == desired_station_name.lower()]

    # Proceed only if the station name exists in the data
    if filtered_gdf.empty:
        st.error("Station name not found.")
        return None

    # Extract the latitude and longitude
    try:
        lat = float(filtered_gdf.iloc[0]['station_la'])
        lon = float(filtered_gdf.iloc[0]['station_lo'])
    except Exception as e:
        st.error(f"Error extracting latitude and longitude: {e}")
        return None

    # Set up the map centered around the station
    m = folium.Map(location=[lat, lon], zoom_start=16, control_scale=True)

    # Add a small red dot at the center of the circle
    CircleMarker(location=[lat, lon], radius=3, color='red', fill=True, fill_color='red').add_to(m)

    # Add a circle of radius 1/2 mile (in meters) around the station
    Circle(location=[lat, lon], radius=804.672).add_to(m)

    # Add a layer control panel to the map
    folium.LayerControl().add_to(m)

    return m

# Streamlit app layout
st.title("Transit Station Selector")

# Create an input box for Station Name
station_name_input = st.text_input("Enter Station Name:", key='station_name_input')

# Create a placeholder for the map
map_placeholder = st.empty()

def update_map():
    desired_station_name = st.session_state.station_name_input
    if desired_station_name:
        map_object = plot_map(desired_station_name, gdf)
        if map_object:
            with map_placeholder:
                st_data = st_folium(map_object, width=700, height=500)
    else:
        st.error("Please enter a station name.")

# Trigger the map update on pressing enter or button click
if station_name_input:
    update_map()

if st.button("Show Map"):
    update_map()

