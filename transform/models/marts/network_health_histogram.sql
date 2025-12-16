{{ config(materialized='table') }}

-- We use a CTE (Common Table Expression) to calculate the rate first
WITH station_stats AS (
  SELECT
    name,
    AVG(CASE WHEN num_bikes_available = 0 THEN 1.0 ELSE 0.0 END) as stockout_rate
  FROM
    {{ source('raw_data', 'status_history') }}
  GROUP BY
    name
)

-- Then we categorize that rate into buckets
SELECT
  name,
  stockout_rate,
  CASE
    WHEN stockout_rate = 1.0 THEN 'Always empty'
    WHEN stockout_rate >= 0.9 THEN '90% - 99% (Critical)'
    WHEN stockout_rate >= 0.8 THEN '80% - 90%'
    WHEN stockout_rate >= 0.7 THEN '70% - 80%'
    WHEN stockout_rate >= 0.6 THEN '60% - 70%'
    WHEN stockout_rate >= 0.5 THEN '50% - 60%'
    WHEN stockout_rate >= 0.4 THEN '40% - 50%'
    WHEN stockout_rate >= 0.3 THEN '30% - 40%'
    WHEN stockout_rate >= 0.2 THEN '20% - 30%'
    WHEN stockout_rate >= 0.1 THEN '10% - 20%'
    WHEN stockout_rate >= 0.01 THEN '1% - 10%'
    ELSE '0%'
  END as reliability_bucket
FROM
  station_stats