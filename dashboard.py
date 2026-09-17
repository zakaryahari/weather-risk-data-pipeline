import streamlit as st
import pandas as pd
from datetime import timedelta, datetime


st.set_page_config(page_title="Weather Risk Dashboard", layout="wide")


@st.cache_data
def load_data():
    data = pd.read_csv("data/gold/All_Moroccain_Citys.csv")
    data['time'] = pd.to_datetime(data['time'])
    return data 

print("Loading data...")
data = load_data()


