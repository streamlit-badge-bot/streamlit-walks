import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
from OSGridConverter import grid2latlong

st.title('Wainwrights: Which one should I climb?')
st.markdown("Wainwrights are the 214 English peaks mapped out in Alfred Wainwright's Pictorial Guide to the Lakeland Fells (1955–66). It is popular for walkers to use these routes when climbing a fell in the Lake District. However, with so much choice, how can we narrow down which one to walk up? The purpose of this app is to narrow down the Wainwrights to aid in your next fell climb in the Lake District.")

st.header("Table of all the Wainwrights. The darker the shade of green, the taller the fell is.")
st.markdown("All the Wainwrights have been listed below.")

# Streamlit will perform internal magic so that the data will be downloaded only once and cached for future use
@st.cache
def get_data():
    url = "https://en.wikipedia.org/wiki/List_of_Wainwrights"
    html = pd.read_html(url, index_col=1)
    df = html[1]
    df = df.drop(columns = ['Height Rank', 'Birkett', 'Prom. (m)', 'Prom. (ft)', 'Classification(§\xa0DoBIH codes)'])
    return df
df = get_data()

cm = sns.light_palette("seagreen", as_cmap=True)
st.dataframe(df.style.background_gradient(cmap=cm))

st.markdown("Lets compare the heights on an area chart.")

# Convert OS Grid Reference to Longitude and Latitude
os_grid = df['OS Grid Reference'].to_list()
latitude = [grid2latlong(i).latitude for i in os_grid]
longitude = [grid2latlong(i).longitude for i in os_grid]
l = [[grid2latlong(i).latitude, grid2latlong(i).longitude] for i in os_grid]
lat_lon = pd.DataFrame(l, columns = ['lat','lon'])
st.dataframe(lat_lon)

st.pydeck_chart(pdk.Deck(
    map_style = 'mapbox://styles/mapbox/light-v9',
    
    initial_view_state = pdk.ViewState(
        latitude = 54.45,
        longitude = -3.1,
        zoom = 9,
    ),
    
    layers = [
        pdk.Layer(
            'HexagonLayer',
            data = lat_lon,
            get_position = '[lon, lat]',
            radius = 400,
            elevation_scale = 10,
            elevation_range = [0, 1000],
            pickable = True,
            extruded = True,
        ),
        
        pdk.Layer(
            'ScatterplotLayer',
            data = lat_lon,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius = 400,
        ),
    ],
))
