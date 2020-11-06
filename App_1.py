import streamlit as st
import pandas as pd 
import numpy as np

st.title('Wainwrights: Which one should I climb?')
st.markdown("Welcome to this in-depth introduction to [...].")

url = "https://en.wikipedia.org/wiki/List_of_Wainwrights"
df =  pd.read_html(url, index_col=0)
df
