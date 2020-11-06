import streamlit as st
import pandas as pd 
import numpy as np

st.title('Wainwrights: Which one should I climb?')
st.markdown("Welcome to this in-depth introduction to [...].")

st.markdown("First we will import the Wainwrights, their geographical location, and their heights below.")
url = "https://en.wikipedia.org/wiki/List_of_Wainwrights"
html = pd.read_html(url, index_col=0)
df = html[1]

df
