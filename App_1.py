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

# --------------------------------
# Title
# --------------------------------
st.title('Wainwrights: Which one should I climb?')
st.markdown("Wainwrights are the 214 English peaks mapped out in Alfred Wainwright's Pictorial Guide to the Lakeland Fells (1955–66). It is popular for walkers to use these routes when climbing a fell in the Lake District. However, with so much choice, how can we narrow down which one to walk up? The purpose of this app is to narrow down the Wainwrights to aid in your next fell climb in the Lake District.")

# --------------------------------
# Import Data
# --------------------------------
st.header("Table of all the Wainwrights. The darker the shade of green, the taller the fell is.")
st.markdown("All the Wainwrights have been listed below.")

url = "https://en.wikipedia.org/wiki/List_of_Wainwrights"
html = pd.read_html(url, index_col=1)
df = html[1]
df = df.drop(columns = ['Height Rank', 'Birkett', 'Prom. (m)', 'Prom. (ft)', 'Classification(§\xa0DoBIH codes)'])
df['Latitude'] = df['OS Grid Reference'].apply(lambda x: grid2latlong(x).latitude)
df['Longitude'] = df['OS Grid Reference'].apply(lambda x: grid2latlong(x).longitude)
cm = sns.light_palette("seagreen", as_cmap=True)
st.dataframe(df.style.background_gradient(cmap=cm))

# --------------------------------
# View on a map
# --------------------------------
st.markdown("Lets compare the heights on an area chart.")
st.pydeck_chart(pdk.Deck(
    map_style = 'mapbox://styles/mapbox/light-v9',
    
    initial_view_state = pdk.ViewState(latitude = 54.45, longitude = -3.1, zoom = 9),
    
    layers = pdk.Layer('HexagonLayer', data = df,
#                        colorDomain = [min(df['Height (m)']), max(df['Height (m)'])],
                       get_position = '[Longitude, Latitude]',
                       auto_highlight = True,
                       elevation_scale = 25,
                       pickable = True,
                       elevation_range = [0, 3000],
                       extruded = True,
                       coverage = 1),
))
