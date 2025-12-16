{{ config(materialized='table') }}

SELECT
  snapshot_time,
  SUM(num_bikes_available) as total_fleet_size
FROM
  {{ source('raw_data', 'status_history') }}
GROUP BY
  snapshot_time