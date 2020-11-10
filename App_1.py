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
# st.title("App to select your next Wainwright")
st.header("The Wainwrights are 214 Lake District peaks.")
st.header("(not a beer)")

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
heights = st.sidebar.slider('Select a height (m)', int(df['Height (m)'].min()), int(df['Height (m)'].max()), (int(df['Height (m)'].min()), int(df['Height (m)'].max())))
section = df['Section'].unique()
blank_selection = section[0] | section[1]
section = np.concatenate((blank_selection, section))
st.write(type(section))
section
filter_section = st.sidebar.selectbox("Section", (section))

fig = px.scatter_mapbox(df[(df['Height (m)'] >= heights[0]) & (df['Height (m)'] <= heights[1]) & (df['Section'] == filter_section)],
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

# # Section filter
# section = df['Section'].unique()
# filter_section = st.sidebar.selectbox("Section", (section))

# for i in section:
#     if filter_section == i:
#         fig = px.scatter_mapbox(df[df['Section']==i],
#                         lat = "Latitude",
#                         lon = "Longitude",
#                         hover_name = "Name",
#                         hover_data = ["Height (m)"],
#                         zoom = 9,
#                         height = 300,
#                         color = 'Height (m)',
#                         size = 'Height (m)',
#                         color_continuous_scale = px.colors.cyclical.IceFire,
#                         size_max = 9)
#         fig.update_layout(mapbox_style = "stamen-terrain") # open-street-map # stamen-terrain
#         fig.update_layout(margin = {"r":0,"t":0,"l":0,"b":0})
#         st.plotly_chart(fig, use_container_width = True)
        
#         st.dataframe(df[df['Section']==i])

# # Filter by Height
# height = df['Height (m)'].unique()
# filter_section = st.sidebar.selectbox("Section", (section))

# Filter by Section
# section = df['Section'].unique()
# filter_section = st.selectbox("Section", (section))

# Slider
# heights = st.slider('Select a height (m)', 270, 970, (270, 970))
# st.write('Values:', values)

# --------------------------------
# View on a map
# --------------------------------
st.title("Here are the Wainwrights plotted on a map:")
st.write("The size of the dot represents the height of the Wainwright (the larger the taller). The darker dots also represent taller Wainwrights.")

fig = px.scatter_mapbox(df,
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
st.write("Here's a table of the Wainwrights, ordered by height:")

cm = sns.light_palette("seagreen", as_cmap=True)
st.dataframe(df.style.background_gradient(cmap=cm))
