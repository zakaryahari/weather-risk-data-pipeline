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

