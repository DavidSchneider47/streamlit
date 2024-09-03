#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# Title and description
st.title("WMATA Station Isochrone Map")
st.write(
    "This map displays WMATA rail stations and estimates the amount of land accessible within a 15-minute walk of each station. "
    "Click the station icon for the name of the station and the amount of land that is within a short walk of the station."
)

# Load the generated map HTML file
map_file_path = "wmata_isochrone.html"

# Display the map within the Streamlit app
with open(map_file_path, 'r', encoding='utf-8') as map_file:
    folium_map = map_file.read()

st.components.v1.html(folium_map, width=700, height=500)

