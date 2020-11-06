# import streamlit as st
# import pandas as pd 
# # import numpy as np
# # from lxml import etree as et

# # Title of app
# st.title('Wainwrights')

# url = 'https://en.wikipedia.org/wiki/List_of_Wainwrights'
# html = pd.read_html(url, index_col = 0, encoding = 'lxml')
# # df = html[1]
# # st.write(df)

# # print(df.columns.values)

# # df.drop(columns = ['Section', 'Birkett', 'Prom. (m)', 'Prom. (ft)', 'Classification(§\xa0DoBIH codes)'])


import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf

st.title('S&P 500 App')

st.markdown("""
This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit, yfinance, numpy, matplotlib
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

st.sidebar.header('User Input Features')

# Web scraping of S&P 500 data
#
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')
