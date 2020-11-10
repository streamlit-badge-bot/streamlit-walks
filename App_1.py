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
st.title("Map")

fig = px.scatter_mapbox(df,
                        lat = "Latitude",
                        lon = "Longitude",
                        hover_name = "Name",
                        hover_data = ["Height (m)"],
                        zoom = 9,
                        height = 300,
                        color = 'Height (m)',
                        size = 'Height (m)',
                        color_continuous_scale = px.colors.Greens,
                        size_max = 7)
fig.update_layout(mapbox_style = "stamen-terrain") # open-street-map # stamen-terrain
fig.update_layout(margin = {"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width = True)
