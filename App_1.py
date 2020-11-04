#!/usr/bin/env python
# coding: utf-8

# #### Install streamlit

# In[1]:


# pip install streamlit


# In[2]:


import streamlit as st
import pandas as pd 
import numpy as np


# In[3]:


# Title of app
st.title('Wainwrights')


# In[4]:


url = 'https://en.wikipedia.org/wiki/List_of_Wainwrights'
html = pd.read_html(url, index_col=0)
df = html[1]

display(df)
print(df.columns.values)


# In[5]:


df.drop(columns = ['Section', 'Birkett', 'Prom. (m)', 'Prom. (ft)', 'Classification(§\xa0DoBIH codes)'])


# In[ ]:




