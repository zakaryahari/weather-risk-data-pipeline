import pandas as pd
import numpy as np
import json
import os
import glob



file_paths = glob.glob("data/bronze/citys/*.json")

df = pd.DataFrame()
print(df)

for path in file_paths:

    file_name = os.path.basename(path) 

    with open(path) as file :
        obj = json.load(file)

    city_name = file_name.replace(".json", "") 

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



df['wind_category'] = np.select(wind_conditions, wind_cat_choices, default="Unknown")



df['wind_points'] = np.select(wind_conditions, wind_point_choices, default=0)





