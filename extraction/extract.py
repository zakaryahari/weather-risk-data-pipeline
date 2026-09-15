import pandas as pd
import requests
import json
import os
import glob

url = "https://simplemaps.com/static/data/country-cities/ma/ma.csv"

df = pd.read_csv(url)

# print(df)

df.to_csv("data/maroc_cities.csv" , index=False)

latitude_list = []
longitude_list = []
counter = 0


for index , row in df.iterrows() :

    latitude_list.append(row['lat'])
    longitude_list.append(row['lng'])
    counter += 1

    if len(latitude_list) == 100:
        

        lat_str = ",".join(map(str, latitude_list))
        lng_str = ",".join(map(str, longitude_list))
        
        api_url = "https://api.open-meteo.com/v1/forecast?latitude=" + lat_str + "&longitude=" + lng_str + "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,weather_code&timezone=auto"
        
        print(f"Sending batch {counter}...")
        response = requests.get(api_url)
        
        if response.status_code == 200:
            file_name = f"data/bronze/Cities_{counter}_Bronze.json"
            with open(file_name, "w") as file:
                json.dump(response.json(), file, indent=4)
        

        latitude_list = []
        longitude_list = []
        counter += 1

if len(latitude_list) > 0:

    lat_str = ",".join(map(str, latitude_list))
    lng_str = ",".join(map(str, longitude_list))
    
    api_url = "https://api.open-meteo.com/v1/forecast?latitude=" + lat_str + "&longitude=" + lng_str + "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,weather_code&timezone=auto"
    
    print(f"Sending final leftover batch {counter}...")
    response = requests.get(api_url)
    
    if response.status_code == 200:
        file_name = f"data/bronze/Cities_{counter}_Bronze.json"
        with open(file_name, "w") as file:
            json.dump(response.json(), file, indent=4)


batch_files = glob.glob("data/bronze/Cities_*_Bronze.json")

merged_data = []


for file_path in batch_files:
    with open(file_path, 'r') as file:
        batch_data = json.load(file)
        merged_data.extend(batch_data)


with open("data/bronze/All_Cities_Bronze.json", "w") as file:
    json.dump(merged_data, file, indent=4)


for file_path in batch_files:
    os.remove(file_path)
