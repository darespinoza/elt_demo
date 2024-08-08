{{
    config(
        materialized='incremental',
        unique_key=['timestamp_day']
    )
}}

SELECT
    DATE_TRUNC('day', rod."Time") AS timestamp_day,
	-- Temperature
    AVG(rod."Temperature") AS avg_temperature,
    MAX(rod."Temperature") AS max_temperature,
    MIN(rod."Temperature") AS min_temperature,
    -- Wind_Speed
    AVG(rod."Wind_Speed") AS avg_wind_speed,
    MAX(rod."Wind_Speed") AS max_wind_speed,
    MIN(rod."Wind_Speed") AS min_wind_speed,
    -- Relative_Humidity
    AVG(rod."Relative_Humidity") AS avg_relative_hum,
    MAX(rod."Relative_Humidity") AS max_relative_hum,
    MIN(rod."Relative_Humidity") AS min_relative_hum,
    -- Precipitation
    AVG(rod."Precipitation") AS avg_precipitation,
    MAX(rod."Precipitation") AS max_precipitation,
    MIN(rod."Precipitation") AS min_precipitation
FROM {{ source('demo_source', 'raw_openmeteo_data') }} rod
{% if is_incremental() %}
    WHERE 'timestamp_day' > (select max('timestamp_day') from {{ this }})
{% endif %}
GROUP BY 
    timestamp_day
ORDER BY 
    timestamp_day DESC