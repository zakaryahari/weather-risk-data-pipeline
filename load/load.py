import pandas as pd
from sqlalchemy import create_engine

df_cities = pd.read_csv("data/maroc_cities.csv")
df_gold = pd.read_csv("data/gold/All_Moroccain_Citys.csv")

df_cities = df_cities.drop(columns=["country","iso2","admin_name","capital","population","population_proper"])
df_cities = df_cities.rename(columns={'lat':'latitude' , 'lng' : 'longitude'})
df_cities['city_id'] = range(1, len(df_cities) + 1)
print(df_cities)

merged_df = pd.merge(df_cities , df_gold , on="city")

final_df = merged_df.drop(columns=[ "city" , "latitude_x" , "longitude_x"  , "latitude_y" , "longitude_y"])

print(final_df)

connection_db = "postgresql://admin:admin@localhost:5432/logistics_weather"

engine = create_engine(connection_db)

print(pd.read_sql())

df_cities.to_sql(
    name='cities',    
    con=engine,              
    if_exists='append',      
    index=False        
)

# final_df.to_sql(
#     name='forecasts',    
#     con=engine,              
#     if_exists='append',      
#     index=False        
# )





