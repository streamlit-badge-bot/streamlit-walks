# --------------------------------
# Packages
# --------------------------------
import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
from OSGridConverter import grid2latlong
import plotly.express as px

st.markdown('<style>h1{color: black; text-align:center;}</style>', unsafe_allow_html=True)
st.markdown('<style>h2{color: green; text-align:center;}</style>', unsafe_allow_html=True)
st.markdown('<style>h3{color: black; text-align:center;}</style>', unsafe_allow_html=True)

# --------------------------------
# Title
# --------------------------------
st.title("Wainwrights: Which one should I climb?")
st.header("Wainwrights are the 214 English peaks mapped out in Alfred Wainwright's Pictorial Guide to the Lakeland Fells (1955–66).")

# --------------------------------
# Sidebar
# --------------------------------
# st.sidebar.header("Filter")

# --------------------------------
# Import Data
# --------------------------------
url = "https://en.wikipedia.org/wiki/List_of_Wainwrights"

@st.cache
def load_data():
    html = pd.read_html(url, index_col=[0])
    df = html[1]
    df['Latitude'] = df['OS Grid Reference'].apply(lambda x: grid2latlong(x).latitude)
    df['Longitude'] = df['OS Grid Reference'].apply(lambda x: grid2latlong(x).longitude)
    df = df.drop(columns = ['Birkett', 'Prom. (m)', 'Height (ft)', 'Prom. (ft)', 'Topo Map', 'OS Grid Reference', 'Classification(§\xa0DoBIH codes)'])
    return df

df = load_data()

# --------------------------------
# Table
# --------------------------------
cm = sns.light_palette("seagreen", as_cmap=True)
st.dataframe(df.style.background_gradient(cmap=cm))

# --------------------------------
# View on a map
# --------------------------------
st.markdown("Lets compare the heights on an area chart.")

# st.map(df)

midpoint = (np.average(lat_lon['lat']), np.average(lat_lon['lon']))

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude = midpoint[0],
        longitude = midpoint[1],
        zoom = 11,
        pitch = 50,
    ),
    layers=
    pdk.Layer(
        'HexagonLayer',
        data = lat_lon,
        get_position = '[lon, lat]',
        radius = 200,
        elevation_scale = 40,
        elevation_range = [0, 214],
        pickable = True,
        extruded = True,
        get_color = '[200, 30, 0, 160]',
    ),
))
