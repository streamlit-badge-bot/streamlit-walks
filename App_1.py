import streamlit as st
import pandas as pd 
import numpy as np

url = 'https://en.wikipedia.org/wiki/List_of_Wainwrights'
html = pd.read_html(url, index_col=0)
df = html[1]

display(df)
print(df.columns.values)
