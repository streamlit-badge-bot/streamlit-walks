# --------------------------------
# Packages
# --------------------------------
import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
from OSGridConverter import grid2latlong

# --------------------------------
# Title
# --------------------------------
st.markdown("<h1 style='text-align: center; color: black;'>Wainwrights: Which one should I climb?</h1>", unsafe_allow_html=True)
st.markdown('<style>h2{color: green; text-align:center;}</style>', unsafe_allow_html=True)
st.markdown("Wainwrights are the 214 English peaks mapped out in Alfred Wainwright's Pictorial Guide to the Lakeland Fells (1955–66). It is popular for walkers to use these routes when climbing a fell in the Lake District. However, with so much choice, how can we narrow down which one to walk up? The purpose of this app is to narrow down the Wainwrights to aid in your next fell climb in the Lake District.")

# --------------------------------
# Import Data
# --------------------------------
st.header("The darker the shade of green, the taller the fell is.")

url = "https://en.wikipedia.org/wiki/List_of_Wainwrights"

@st.cache
def load_data():
    html = pd.read_html(url)
    df = html[1]
    df['Latitude'] = df['OS Grid Reference'].apply(lambda x: grid2latlong(x).latitude)
    df['Longitude'] = df['OS Grid Reference'].apply(lambda x: grid2latlong(x).longitude)
    df = df.drop(columns = ['Birkett', 'Prom. (m)', 'Height (ft)', 'Prom. (ft)', 'Topo Map', 'OS Grid Reference', 'Classification(§\xa0DoBIH codes)'])
    return df

df = load_data()

# --------------------------------
# Sidebar
# --------------------------------
# st.sidebar.header("Filter")

cm = sns.light_palette("seagreen", as_cmap=True)
st.dataframe(df.style.background_gradient(cmap=cm))

# --------------------------------
# View on a map
# --------------------------------
st.markdown("Lets compare the heights on an area chart.")

# st.map(df)

lat_lon = pd.DataFrame(df)
lat_lon = lat_lon.drop(columns = ['Name', 'Section', 'Height (m)'])
lat_lon

df_1 = pd.DataFrame(np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4], columns=['lat', 'lon'])
df_1


midpoint = (np.average(lat_lon['Latitude']), np.average(lat_lon['Longitude']))

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude = midpoint[0],
        longitude = midpoint[1],
        zoom = 11,
        pitch = 50,
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data = lat_lon,
            get_position = '[Longitude, Latitude]',
            radius = 200,
            elevation_scale = 40,
            elevation_range = [0, 214],
            pickable = True,
            extruded = True,
            get_color = '[200, 30, 0, 160]',
        ),
#         pdk.Layer(
#             'ScatterplotLayer',
#             data = lat_lon,
#             get_position = '[Longitude, Latitude]',
#             get_color = '[200, 30, 0, 160]',
#             get_radius = 200,
#         ),
    ],
))



import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA_URL = (
    "Downloads\\Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.markdown("<h1 style='text-align: center; color: black;'>Geographic Data</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: black;'>Dataset of Vehicle Collisions</h1>", unsafe_allow_html=True)
st.markdown('<style>h2{color: blue; text-align:center;}</style>', unsafe_allow_html=True)


@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[["CRASH DATE", "CRASH TIME"]])
    data.dropna(subset=["LATITUDE", "LONGITUDE"], inplace=True)
    data.drop(data[data['LATITUDE'] == 0].index, inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash date_crash time': 'date/time'}, inplace=True)
    data.rename(columns={'number of persons injured': 'injured_persons'}, inplace=True)
    data.rename(columns={'number of pedestrians injured': 'injured_pedestrians'}, inplace=True)
    data.rename(columns={'number of cyclist injured': 'injured_cyclists'}, inplace=True)
    data.rename(columns={'number of motorist injured': 'injured_motorists'}, inplace=True)
    return data

data = load_data(600000)

st.sidebar.header("jgamboa")
st.header("Number of Injured Person x Collision")

st.sidebar.header("Filter Parameters")
st.sidebar.header("where are most people injure?")
#injured_people = st.sidebar.slider("# Person injured in Collisions", 0, 9)
injured_people = st.sidebar.number_input("Number Person injured in Collisions", step=1, min_value=0, max_value=9, value=1)
st.map(data.query('injured_persons > @injured_people')[["latitude", "longitude"]].dropna(how="any"))

st.sidebar.header("How many collision occur during a given time of day?")
hour = st.sidebar.number_input("Insert TIME-HOUR", step=1, min_value=0, max_value=24, value=1)

data = data[data['date/time'].dt.hour == hour]
st.header("Vehicle Collision between %i:00 and %i:00" % (hour, (hour + 1) % 24))

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,

    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data[['date/time', 'latitude', 'longitude']],
            get_position=["longitude", "latitude"],
            auto_highlight=True,
            radius=100,
            extruded=True,
            pickable=True,
            elevation_scale=4,
            elevation_range=[0, 1000],
        ),
    ],
))

st.header("Histogram by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
    ]

hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({"minute": range(60), "crashes": hist})

fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

st.sidebar.header("Dangerous streets")
st.header("List Most injured people x Street")
select = st.sidebar.selectbox('Affected type of person', ['Pedestrians', 'Cyclist', 'Motorists'])

if select == 'Pedestrians':
    st.write(data.query("injured_pedestrians >= 1")[["on street name", "injured_pedestrians"]].sort_values(
        by=['injured_pedestrians'], ascending=False).dropna(how="any")[:7])

elif select == 'Cyclists':
    st.write(
        data.query("injured_cyclists >= 1")[["on street name", "injured_cyclists"]].sort_values(
            by=['injured_cyclists'], ascending=False).dropna(how="any")[:7])

else:
    st.write(data.query("injured_motorists >= 1")[["on street name", "injured_motorists"]].sort_values(
        by=['injured_motorists'], ascending=False).dropna(how="any")[:7])

if st.checkbox("Show Data", False):
    st.subheader('Raw Data')
    st.write(data)

st.sidebar.markdown("libraries used: **streamlit**, **pandas**, **numpy**, **pydeck**, **plotly**")
st.sidebar.markdown("**Dataset:** Rows: 1.69M  Columns: 29")
st.sidebar.markdown("Update: June 26, 2020")
