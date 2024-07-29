#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import folium
from folium import CircleMarker, Circle
import pandas as pd
from streamlit_folium import st_folium

# Read the .csv file into a DataFrame
gdf = pd.read_csv('LIRR for streamlit.csv')  # Update the file path as needed

# Extract and sort the list of station names
station_names = sorted(gdf['station_name'].unique())

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
    m = folium.Map(location=[lat, lon], zoom_start=15, control_scale=True)  # Adjusted zoom_start to 15

    # Add a small red dot at the center of the circle
    CircleMarker(location=[lat, lon], radius=3, color='red', fill=True, fill_color='red').add_to(m)

    # Add a circle of radius 1/2 mile (in meters) around the station
    Circle(location=[lat, lon], radius=804.672).add_to(m)

    # Add a layer control panel to the map
    folium.LayerControl().add_to(m)

    return m

# Streamlit app layout
st.title("Transit Station Selector Prototype")

# Additional text in a slightly smaller font
st.markdown(
    """
    <p style="font-size:14px;">
    This tool is a prototype web application that provides geographic information on areas within a 1/2 mile radius of Long Island Rail Road transit stations as well as facts about each station. Data sources include General Transit Feed Specification, the 2022 National Transit Database Facility Inventory and OpenStreetMap. Missing station information appears as “ ” Browse through the list below or type in a station name to select a station. For more information visit <a href="http://www.transitorienteddiscoveries.com" target="_blank">www.transitorienteddiscoveries.com</a>.
    </p>
    """, unsafe_allow_html=True
)

# Create a selectbox for Station Name
station_name_input = st.selectbox("Select Station Name:", station_names, key='station_name_input')

# Create a placeholder for the map
map_placeholder = st.empty()

def update_map():
    desired_station_name = st.session_state.station_name_input
    if desired_station_name:
        map_object = plot_map(desired_station_name, gdf)
        if map_object:
            with map_placeholder:
                st_data = st_folium(map_object, width=700, height=500)
            
            # Fetch and display station details
            station_details = gdf[gdf['station_name'].str.lower() == desired_station_name.lower()].iloc[0]

            # Replace NaN with empty string and get details
            station_name = station_details.get('station_name', '')
            primary_mode_served = station_details.get('primary_mode_served', '')
            agency = station_details.get('agency', '')
            line = station_details.get('line', '')
            facility_type = station_details.get('facility_type', '')
            full_address = station_details.get('full_address', '')
            county = station_details.get('county', '')
            year_built = station_details.get('year_built', '')
            square_feet = station_details.get('square_feet', '')
            
            # Convert NaN to empty string
            if pd.isna(square_feet):
                square_feet = ''

            st.markdown(f"""
                {station_name} is a {primary_mode_served} station operated by {agency} on the {line}. 
                It is a {facility_type} located at {full_address} in {county}. 
                It was built or renovated in {year_built} and is approximately {square_feet} square feet.
            """)
    else:
        st.error("Please select a station name.")

# Trigger the map update on selection change or button click
if station_name_input:
    update_map()

if st.button("Show Map"):
    update_map()

