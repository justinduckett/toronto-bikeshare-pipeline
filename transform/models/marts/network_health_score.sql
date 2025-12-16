{{ config(materialized='table') }}

SELECT
  snapshot_time,
  -- Calculate the % of stations that had at least 1 bike
  -- NULLIF prevents "division by zero" errors
  COUNTIF(num_bikes_available > 0) / NULLIF(COUNT(*), 0) as network_health_score
FROM
  {{ source('raw_data', 'status_history') }}
WHERE
  -- Exclude inactive stations so they don't drag the score down
  num_bikes_available > 0 OR num_docks_available > 0
GROUP BY
  snapshot_time