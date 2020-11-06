import pandas as pd

url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
html = pd.read_html(url, header = 0)
df = html[0]
