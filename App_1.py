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

@st.cache
def load_data():
    html = pd.read_html(url, index_col=1)
    df = html[1]
    df['latitude'] = df['OS Grid Reference'].apply(lambda x: grid2latlong(x).latitude)
    df['longitude'] = df['OS Grid Reference'].apply(lambda x: grid2latlong(x).longitude)
    df = df.drop(columns = ['Height Rank', 'Birkett', 'Prom. (m)', 'Height (ft)', 'Prom. (ft)', 'Topo Map', 'OS Grid Reference', 'Classification(§\xa0DoBIH codes)'])
    return df

df = load_data()

cm = sns.light_palette("seagreen", as_cmap=True)
st.dataframe(df.style.background_gradient(cmap=cm))

# --------------------------------
# View on a map
# --------------------------------
st.markdown("Lets compare the heights on an area chart.")

st.map(df)

df = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=37.76,
        longitude=-122.4,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=df,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
))
