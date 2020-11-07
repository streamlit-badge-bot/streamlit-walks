import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

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
# df_plot = df.set_index("name",drop=True,inplace=True)
# st.area_chart(data=df, width=0, height=0, use_container_width=True)
st.area_chart(data=df['Height (m)'])

fig = ff.create_distplot(df, group_labels, bin_size=[.1, .25, .5])
st.plotly_chart(fig, use_container_width=True)
