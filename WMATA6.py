#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import requests

# Set the page configuration to wide mode with a dark theme
st.set_page_config(layout="wide", page_title="WMATA Station Area Parking Map", initial_sidebar_state="collapsed")

# Set the dark background style and custom title style
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #ffcc00;  /* Bright yellow for contrast */
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page title with custom class
st.markdown('<div class="title">WMATA Station Area Parking Map</div>', unsafe_allow_html=True)

# Add the description text below the title
st.markdown("""
This prototype identifies surface parking lots and parking garages located within 1/4 mile of a WMATA rail station. Zoom in to explore an area and click the icon for a summary of land devoted to parking around each station.
""")

# Function to load the map from a URL
def load_map():
    url = "https://raw.githubusercontent.com/DavidSchneider47/streamlit/main/WMATA_map1.html"  # Replace with your actual URL
    response = requests.get(url)
    html_content = response.text
    st.components.v1.html(html_content, width=1000, height=1000)

# Display the map
load_map()

