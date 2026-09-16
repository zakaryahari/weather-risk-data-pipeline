Create database weather_db;

USE weather_db;

DROP TABLE IF EXISTS weather_gold;

CREATE TABLE cities (
    city_id INT PRIMARY KEY,
    city VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT
);

SELECT * FROM cities;

CREATE TABLE forecasts (
    forecast_id SERIAL PRIMARY KEY, 
    city_id INT,
    time DATE,
    temperature_2m_max FLOAT,
    precipitation_sum FLOAT,
    wind_speed_10m_max FLOAT,
    temp_category VARCHAR(50),
    precip_category VARCHAR(50),
    wind_category VARCHAR(50),
    risk_score INT,
    extracted_at TIMESTAMP,
    FOREIGN KEY (city_id) REFERENCES cities (city_id)
);