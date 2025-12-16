{{ config(materialized='table') }}

SELECT
  station_id,
  name,
  lat,
  lon,
  AVG(num_bikes_available) as avg_bikes,
  MAX(num_bikes_available + num_docks_available) as total_capacity,
  CASE
    WHEN AVG(num_bikes_available) <= 1 THEN 'Critical (Red)'
    WHEN AVG(num_bikes_available) <= 3 THEN 'Low (Yellow)'
    ELSE 'Good (Green)'
  END as availability_bucket
FROM
  {{ source('raw_data', 'status_history') }}
WHERE
  -- Only look at the last 7 days of data
  TIMESTAMP(snapshot_time) >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY
  station_id, name, lat, lon