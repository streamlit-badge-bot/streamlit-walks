import streamlit as st
import pandas as pd 
import numpy as np

st.title('Wainwrights: Which one should I climb?')
st.markdown("Welcome to this in-depth introduction to [...].")

st.sidebar.header('User Input Features')

# Cache data for future use
@st.cache
def get_data():
    url = "https://en.wikipedia.org/wiki/List_of_Wainwrights"
    return pd.read_html(url, index_col=0)
df = get_data()

st.header("Customary quote")
st.markdown("> I just love to go home, no matter where I am [...]")

st.dataframe(df.head())
