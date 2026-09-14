import pandas as pd
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
