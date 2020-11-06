import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Wainwrights: Which one should I climb?')

st.markdown("First we will import the Wainwrights, their geographical location, and their heights below.")

# Streamlit will perform internal magic so that the data will be downloaded only once and cached for future use
@st.cache
def get_data():
    url = "https://en.wikipedia.org/wiki/List_of_Wainwrights"
    html = pd.read_html(url, index_col=0)
    df = html[1]
    return df
df = get_data()

cm = sns.light_palette("husl", as_cmap=True)
s = df.style.background_gradient(cmap=cm)
s
