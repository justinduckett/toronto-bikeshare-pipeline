# End-to-End Analytics Engineering Pipeline: Toronto Bike Share

This repository hosts a fully automated, serverless ELT pipeline that captures real-time transit data from the Toronto Parking Authority.

It demonstrates a modern Analytics Engineering workflow: ingesting raw API data via Python, warehousing it in Google BigQuery, and using dbt (data build tool) to transform raw records into clean, business-ready data models for visualization.

View the Live Dashboard: [Link to Looker Studio Report](https://lookerstudio.google.com/reporting/ee66c00f-c017-4a8d-9249-72a67b1ba3a6)

## Features

- **ELT Architecture:** Moves away from brittle "Extract-Transform-Load" scripts to a robust "Extract-Load-Transform" pattern using dbt.

- **Serverless Orchestration:** Uses GitHub Actions to schedule the full pipeline (Ingestion + Transformation) hourly.

- **Modular Data Modeling:** Logic is version-controlled in dbt models, not hidden in dashboard configs.

- **Infrastructure as Code:** The pipeline dynamically authenticates via Service Accounts and configures the dbt profile at runtime for secure CI/CD execution.

- **Cost Optimization:** Architected to run entirely on free-tier resources ($0.00/month).

## Tech Stack

- **Ingestion:** Python (Pandas, Requests, pandas-gbq)

- **Transformation:** dbt Core (SQL, Jinja, YAML)

- **Warehousing:** Google BigQuery

- **Orchestration:** GitHub Actions (Cron Scheduler)

- **Visualization:** Looker Studio

## Architecture Overview

The pipeline runs automatically every hour ("set and forget"):

1. **Extract & Load (Python):**

    - Fetches live station status from the GBFS API.

    - Appends raw JSON data into the status_history table in BigQuery.

2. **Transform (dbt):**

    - GitHub Actions installs dbt and authenticates dynamically.

    - Runs SQL models to calculate fleet size, station health, and stockout rates.

    - Materializes final tables in a separate bike_data_dbt dataset.

3. **Visualize:**

    - Looker Studio reads from the pre-calculated dbt tables for high-performance dashboards.

## Installation & Setup
Follow these steps to replicate this pipeline locally.

### 1. Clone the Repository
```
git clone https://github.com/yourusername/toronto-bikeshare-pipeline.git
cd toronto-bikeshare-pipeline
```
### 2. Install Dependencies

This project uses dbt-bigquery alongside standard Python libraries.

```
pip install -r requirements.txt
```

### 3. Configure Credentials (Local)

To run dbt locally, you need a ```profiles.yml``` file in your ```~/.dbt/``` folder pointing to your Google Cloud Project.

- Project: toronto-bikeshare-analytics

- Dataset: bike_data_dbt

- Auth: Service Account JSON Key

### 4. Run the Pipeline Locally

Step 1: Ingest Data

```
python main.py
```
Step 2: Transform Data

```
cd transform
dbt run
```

## Transformation Logic (dbt)
Instead of complex SQL queries living in the visualization tool, logic is defined in modular dbt models.

Example: Calculating Station Reliability: ```models/marts/network_health_histogram.sql```

```
SQL

WITH station_stats AS (
  SELECT
    name,
    AVG(CASE WHEN num_bikes_available = 0 THEN 1.0 ELSE 0.0 END) as stockout_rate
  FROM
    {{ source('raw_data', 'status_history') }}
  GROUP BY
    name
)

SELECT
  name,
  stockout_rate,
  CASE
    WHEN stockout_rate >= 0.9 THEN 'Critical (90%+ Empty)'
    WHEN stockout_rate >= 0.7 THEN 'Warning (70-90% Empty)'
    ELSE 'Healthy'
  END as reliability_bucket
FROM
  station_stats
  ```

## Results & Impact

- Automated Data Quality: The pipeline ensures only clean, tested data reaches the dashboard.

- Operational Insight: Identified that ~8% of the network consists of inactive "Zombie Stations" (0 bikes available for >7 days).

- Professional Workflow: Demonstrates ability to mix Python scripting with enterprise-standard transformation tools (dbt) and CI/CD practices.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Data provided by the Toronto Parking Authority via the Open Data Portal.

- Built using the global GBFS (General Bikeshare Feed Specification) standard.