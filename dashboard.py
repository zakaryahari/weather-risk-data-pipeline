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
