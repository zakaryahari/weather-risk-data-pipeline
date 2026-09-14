import pandas as pd
import requests
import json

df = pd.read_csv("data/maroc_cities.csv")

for index , row in df.iterrows() :
    print(row['city'],row['lat'],row['lng'])

    url = "https://api.open-meteo.com/v1/forecast?latitude="+ row['lat'] +"&longitude=" + row['lng'] + "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max,weather_code&timezone=auto"

    try : 
        
        responde = requests.get(url)

        if responde.status_code == 200 :

            responde = responde.json()

            with open("data/bronze/citys/casa.json", "w") as file:
                json.dump(responde, file, indent=4)
        else : 
            print("Request failed:", responde.status_code)

    except requests.exceptions.RequestException as e:
        print("Something went wrong:", e)

# print(responde)