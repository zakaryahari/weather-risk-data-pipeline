import pandas as pd

url = "https://simplemaps.com/static/data/country-cities/ma/ma.csv"

df = pd.read_csv(url)

print(df)

df.to_csv("data/maroc_cities.csv" , index=False)