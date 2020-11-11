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

st.markdown('<style>h1{color: green; text-align:center;}</style>', unsafe_allow_html=True)
st.markdown('<style>h2{color: black; text-align:center;}</style>', unsafe_allow_html=True)
st.markdown('<style>h3{color: black; text-align:center;}</style>', unsafe_allow_html=True)

# --------------------------------
# Title
# --------------------------------
# st.title("App to select your next Wainwright")
st.title("The Wainwrights are Lake District peaks.")
st.subheader("(not a Lancashire beer)")

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
# Sidebar
# --------------------------------
st.sidebar.title("Filter")

# Height filter
heights = st.sidebar.slider('Select a height (m)', 
                            int(df['Height (m)'].min()), 
                            int(df['Height (m)'].max()), 
                            (int(df['Height (m)'].min()), 
                             int(df['Height (m)'].max()))
                           )

section = df['Section'].unique()
filter_section = st.sidebar.selectbox("Select a geographical area (Central and West, East, North or South", (section))

selected = df[(df['Height (m)'] >= heights[0]) & (df['Height (m)'] <= heights[1]) & (df['Section'] == filter_section)]

names = selected['Name'].unique()
names = sorted(names, reverse = False)

for i in names:
    st.sidebar.checkbox(i)
    
# --------------------------------
# View on a map
# --------------------------------
st.header("View and filter on a map:")
st.write("The shade size of the dot represent the height of the Wainwright.")

fig = px.scatter_mapbox(selected,
                        lat = "Latitude",
                        lon = "Longitude",
                        hover_name = "Name",
                        hover_data = ["Height (m)"],
                        zoom = 8,
                        height = 300,
                        color = 'Height (m)',
                        size = 'Height (m)',
                        color_continuous_scale = px.colors.cyclical.IceFire,
                        size_max = 9)
fig.update_layout(mapbox_style = "stamen-terrain") # open-street-map # stamen-terrain
fig.update_layout(margin = {"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width = True)

# --------------------------------
# Table
# --------------------------------
st.header("View and filter table:")

cm = sns.light_palette("seagreen", as_cmap=True)
st.dataframe(selected.style.background_gradient(cmap=cm))
