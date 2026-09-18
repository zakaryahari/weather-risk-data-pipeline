import streamlit as st
import pandas as pd
from datetime import timedelta, datetime
import plotly.express as px


st.set_page_config(page_title="Weather Risk Dashboard", layout="wide")


@st.cache_data
def load_data():
    DB_URL = "postgresql://admin:admin@postgres_db:5432/logistics_weather"
    data_cites = pd.read_sql("SELECT * FROM cities", con=DB_URL)
    data_forecase = pd.read_sql("SELECT * FROM forecasts", con=DB_URL)

    data = data_cites.merge(data_forecase ,on="city_id")

    return data

st.title("Weather Logistics Risk Dashboard")

st.logo(image="data/youcode.png",
            icon_image="data/youcode.png")

df = load_data()



available_cities = df['city'].unique()
available_risks = df['risk_score'].unique()
available_risks.sort()
available_date = df['time'].unique()

filterd_data = df.copy()


st.subheader("Overview Statistics")


kpi1, kpi2, kpi3, kpi4 = st.columns(4)


total_cities = len(filterd_data['city'].unique())
max_risk = filterd_data['risk_score'].max()
max_temp = filterd_data['temperature_2m_max'].max()
max_wind = filterd_data['wind_speed_10m_max'].max()


kpi1.metric(label="Cities Tracked", value=total_cities)
kpi2.metric(label="Highest Risk Score", value=f"{max_risk}")
kpi3.metric(label="Max Temp (°C)", value=f"{max_temp}")
kpi4.metric(label="Peak Wind Gusts", value=f"{max_wind}")

st.divider()

selected_cities = st.sidebar.multiselect(
    "Choose City Plz :"
    ,available_cities
)


selected_risk = st.sidebar.multiselect(
    "Choose Risk Score :"
    ,available_risks
)


selected_date = st.sidebar.multiselect(
    "Choose datetime Plz :"
    ,available_date
)

if selected_cities :
    filterd_data = filterd_data[filterd_data['city'].isin(selected_cities)]

if selected_risk :
    filterd_data = filterd_data[filterd_data['risk_score'].isin(selected_risk)]

if selected_date :
    filterd_data = filterd_data[filterd_data['time'].isin(selected_date)]


st.dataframe(filterd_data)


col1, col2 = st.columns(2)
st.divider() 

with col1 :
    st.subheader("Precipitation Trends by City")

    fig = px.bar(
        filterd_data,
        x="city",
        y="precipitation_sum",
        color="city"
)
col1.plotly_chart(fig, use_container_width=True)

with col2 :
    st.subheader("Temperature Forecast")

    fig2 = px.line(
        filterd_data,
        x="city",
        y="temperature_2m_max",
        color="city",
        markers=True
)

col2.plotly_chart(fig2, use_container_width=True)


st.subheader("Wind Speed Forecast")

fig3 = px.line(
    filterd_data,
    x="city",
    y="wind_speed_10m_max"
)

st.plotly_chart(fig3, use_container_width=True)

fig4 = px.scatter_map(
    filterd_data,
        lat="latitude",
        lon="longitude",
        color="risk_score",
        size="risk_score",    
        hover_name="city",  
        hover_data={
            "latitude": False,  
            "longitude": False,
            "risk_score": True,
            "temperature_2m_max": True,
            "wind_speed_10m_max": True,
            "precipitation_sum": True
        },
        zoom=5,
        center={"lat": 31.7917, "lon": -7.0926},
        map_style="carto-darkmatter",
        height=900
)

st.plotly_chart(fig4 , use_container_width=True)
