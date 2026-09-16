import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert

connection_db = "postgresql://admin:admin@localhost:5432/logistics_weather"

engine = create_engine(connection_db)



df_cities = pd.read_csv("data/maroc_cities.csv")
df_gold = pd.read_csv("data/gold/All_Moroccain_Citys.csv")

df_cities = df_cities.drop(columns=["country","iso2","admin_name","capital","population","population_proper"])
df_cities = df_cities.rename(columns={'lat':'latitude' , 'lng' : 'longitude'})




with open("load/Weather_DB.session.sql", "r") as file:
    schema_query = file.read()

with engine.begin() as connection:
    connection.execute(text(schema_query))
    print("Database schema verified and ready!")


with engine.begin() as connection:
    for index, row in df_cities.iterrows(): 
        query = "INSERT INTO cities (city,latitude,longitude)" \
        "VALUES (:city, :latitude, :longitude) " \
        "ON CONFLICT (city) DO UPDATE SET " \
        "city = EXCLUDED.city," \
        "latitude = EXCLUDED.latitude," \
        "longitude = EXCLUDED.longitude;"

        connection.execute(
            text(query), 
            {"city": row['city'],
            "latitude": row['latitude'], 
            "longitude": row['longitude']}
        )

db_cities = pd.read_sql("SELECT city_id, city FROM cities", con=engine)

merged_df = pd.merge(db_cities , df_gold , on="city")

# final_df = merged_df.drop(columns=[ "city" , "latitude_x" , "longitude_x"  , "latitude_y" , "longitude_y"])

print(merged_df)


