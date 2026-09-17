import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.postgresql import insert

connection_db = "postgresql://admin:admin@postgres_db:5432/logistics_weather"

engine = create_engine(connection_db)



df_cities = pd.read_csv("/opt/airflow/data/maroc_cities.csv")
df_gold = pd.read_csv("/opt/airflow/data/gold/All_Moroccain_Citys.csv")

df_cities = df_cities.drop(columns=["country","iso2","admin_name","capital","population","population_proper"])
df_cities = df_cities.rename(columns={'lat':'latitude' , 'lng' : 'longitude'})




with open("/opt/airflow/scripts/Weather_DB.session.sql", "r") as file:
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

print("Cities data inserted/updated successfully!")

db_cities = pd.read_sql("SELECT city_id, city FROM cities", con=engine)

merged_df = pd.merge(db_cities , df_gold , on="city")

final_df = merged_df.drop(columns=[ "city" , "latitude" , "longitude"])


with engine.begin() as connection:
    for index, row in final_df.iterrows(): 

        query = "INSERT INTO forecasts (city_id, time, temperature_2m_max, precipitation_sum, wind_speed_10m_max, temp_category, precip_category, wind_category, risk_score, extracted_at) " \
                "VALUES (:city_id, :time, :temperature_2m_max, :precipitation_sum, :wind_speed_10m_max, :temp_category, :precip_category, :wind_category, :risk_score, :extracted_at) " \
                "ON CONFLICT (city_id, time) DO UPDATE SET " \
                "temperature_2m_max = EXCLUDED.temperature_2m_max, " \
                "precipitation_sum = EXCLUDED.precipitation_sum, " \
                "wind_speed_10m_max = EXCLUDED.wind_speed_10m_max, " \
                "temp_category = EXCLUDED.temp_category, " \
                "precip_category = EXCLUDED.precip_category, " \
                "wind_category = EXCLUDED.wind_category, " \
                "risk_score = EXCLUDED.risk_score, " \
                "extracted_at = EXCLUDED.extracted_at;"

        connection.execute(
            text(query), 
            {
                "city_id": row['city_id'],
                "time": row['time'],
                "temperature_2m_max": row['temperature_2m_max'],
                "precipitation_sum": row['precipitation_sum'],
                "wind_speed_10m_max": row['wind_speed_10m_max'],
                "temp_category": row['temp_category'],
                "precip_category": row['precip_category'],
                "wind_category": row['wind_category'],
                "risk_score": row['risk_score'],
                "extracted_at": row['extracted_at']
            }
        )

print("Forecasts data inserted/updated successfully!")
# print(final_df) 




