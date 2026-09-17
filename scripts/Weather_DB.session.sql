DROP TABLE IF EXISTS forecasts;
DROP TABLE IF EXISTS cities;


CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city VARCHAR(100) UNIQUE NOT NULL,
    latitude FLOAT,
    longitude FLOAT
);


CREATE TABLE forecasts (
    forecast_id SERIAL PRIMARY KEY, 
    city_id INT REFERENCES cities (city_id),
    time DATE,
    temperature_2m_max FLOAT,
    precipitation_sum FLOAT,
    wind_speed_10m_max FLOAT,
    temp_category VARCHAR(50),
    precip_category VARCHAR(50),
    wind_category VARCHAR(50),
    risk_score INT,
    extracted_at TIMESTAMP,
    CONSTRAINT unique_city_time UNIQUE (city_id, time)
);
