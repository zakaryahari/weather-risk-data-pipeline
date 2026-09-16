import pandas as pd
import numpy as np
import json
import os
import glob


All_Cites_Name = pd.read_csv("data/maroc_cities.csv")
with open("data/bronze/All_Cities_Bronze.json") as file :
    All_Cites_Data = json.load(file)

df = pd.DataFrame()
# print(df)   

for index,obj in enumerate(All_Cites_Data):

    # print(All_Cites_Name.iloc[index]['city'])

    city_name = All_Cites_Name.iloc[index]['city']

    tab = pd.DataFrame(obj['daily'])
    tab['city'] = city_name
    tab['latitude'] = obj['latitude']
    tab['longitude'] = obj['longitude']
    tab['extracted_at'] = pd.Timestamp.now()

    tab.fillna(0)

    df = pd.concat([df , tab] , ignore_index=True)

df.to_csv("data/silver/All_Moroccain_Citys.csv" , index=False)


# print(df.head())


wind_conditions = [
    (df['wind_speed_10m_max'] < 20),
    (df['wind_speed_10m_max'] >= 20) & (df['wind_speed_10m_max'] <= 40),
    (df['wind_speed_10m_max'] > 40)
]
wind_cat_choices = ["Calm", "Moderate", "High"]
wind_point_choices = [0, 15, 40]


precip_conditions = [
    (df['precipitation_sum'] == 0.0),
    (df['precipitation_sum'] >= 0.1) & (df['precipitation_sum'] <= 5.0),
    (df['precipitation_sum'] > 5.0)
]
precip_cat_choices = ["Dry", "Light Rain", "Heavy Rain"]
precip_point_choices = [0, 20, 45]


temp_conditions = [
    (df['temperature_2m_max'] >= 5) & (df['temperature_2m_max'] <= 35),
    (df['temperature_2m_max'] > 35),
    (df['temperature_2m_max'] < 5)
]
temp_cat_choices = ["Normal", "Extreme Heat", "Extreme Cold"]
temp_point_choices = [0, 7, 15]


df['wind_category'] = np.select(wind_conditions, wind_cat_choices, default="Unknown")
df['precip_category'] = np.select(precip_conditions, precip_cat_choices, default="Unknown")
df['temp_category'] = np.select(temp_conditions, temp_cat_choices, default="Unknown")


df['wind_points'] = np.select(wind_conditions, wind_point_choices, default=0)
df['precip_points'] = np.select(precip_conditions, precip_point_choices, default=0)
df['temp_points'] = np.select(temp_conditions, temp_point_choices, default=0)


df['risk_score'] = df['wind_points'] + df['precip_points'] + df['temp_points']
df = df.drop(columns=['wind_points', 'precip_points', 'temp_points',"temperature_2m_min", "precipitation_probability_max", "wind_gusts_10m_max", "weather_code"])


df.to_csv("data/gold/All_Moroccain_Citys.csv" , index=False)
