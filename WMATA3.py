#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st

# Set the page configuration to wide mode with a dark theme
st.set_page_config(layout="wide", page_title="WMATA Station Area Parking Map", initial_sidebar_state="collapsed")

# Set the dark background style
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Page title
st.title('WMATA Station Area Parking Map')

# Add the description text below the title
st.markdown("""
This prototype identifies surface parking lots and parking garages located within 1/4 mile of a WMATA rail station. Zoom in to explore an area and click the icon for a summary of land devoted to parking around each station.
""")

# Load the pre-generated map HTML file
def load_map():
    with open('wmata_map1.html', 'r') as f:
        html_content = f.read()
    st.components.v1.html(html_content, width=1000, height=1000)

# Display the map
load_map()

