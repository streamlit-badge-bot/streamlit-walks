pip install lxml
import streamlit as st
import pandas as pd 
# import numpy as np
# from lxml import etree as et

# Title of app
st.title('Wainwrights')

url = 'https://en.wikipedia.org/wiki/List_of_Wainwrights'
html = pd.read_html(url, index_col=0)
# df = html[1]
# st.write(df)

# print(df.columns.values)

# df.drop(columns = ['Section', 'Birkett', 'Prom. (m)', 'Prom. (ft)', 'Classification(§\xa0DoBIH codes)'])



