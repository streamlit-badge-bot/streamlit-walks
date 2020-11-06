import streamlit as st
import pandas as pd 
import numpy as np

st.title('Wainwrights')

@st.cache
def get_data():
    url = "https://en.wikipedia.org/wiki/List_of_Wainwrights"
    return pd.read_html(url, index_col=0)
df = get_data()
