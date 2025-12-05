# End-to-End Serverless Data Pipeline: Toronto Bike Share Analytics

This repository contains a fully automated, serverless data pipeline that captures real-time transit data from the Toronto Parking Authority. It moves away from manual data extraction to a cloud-native architecture, building a historical data warehouse in Google BigQuery and visualizing network performance in a live dashboard.

View the Live Dashboard: [Link to Looker Studio Report]

## Features

- Serverless Orchestration: Uses GitHub Actions to schedule and run the pipeline hourly without needing a dedicated server.
- Automated Ingestion: Fetches real-time data from the Bike Share Toronto GBFS API (General Bikeshare Feed Specification).
- Data Enrichment: Merges dynamic status feeds (bike counts) with static station information (names, coordinates) for geospatial analysis.
- Schema Evolution: Automatically detects and adapts to new data fields in BigQuery, preventing pipeline failures.
- Cost Optimization: Architected to run entirely on free-tier resources ($0.00/month).

## Prerequisites

- Python 3.x: The pipeline logic is written in Python.
- Google Cloud Platform (GCP) Account: You need a project with BigQuery enabled.
- GitHub Account: To host the repository and run the automation workflows.
- Dependencies: The project relies on:
  - `pandas` (for data transformation)
  - `pandas-gbq` (for loading to BigQuery)
  - `requests` (for API fetching)

## Installation & Setup

Follow these steps to replicate this pipeline in your own environment.

### 1. Clone the Repository

Download the project files to your computer or cloud environment:
```
git clone [https://github.com/yourusername/toronto-bikeshare-pipeline.git](https://github.com/yourusername/toronto-bikeshare-pipeline.git)
cd toronto-bikeshare-pipeline
```


### 2. Install Dependencies

Install the required libraries using pip:
```
pip install -r requirements.txt
```

- What this does: Installs the necessary Python packages to run the extraction script locally.

### 3. Configure Google Cloud (BigQuery)

- Go to the Google Cloud Console.
- Create a new project (e.g., toronto-bikeshare-analytics).
- Enable the BigQuery API.
- Create a Service Account with "BigQuery Admin" permissions.
- Download the Service Account Key as a JSON file.

### 4. Configure GitHub Secrets

- Go to your GitHub Repository settings > Secrets and variables > Actions.
- Create a new repository secret named GCP_SERVICE_ACCOUNT_KEY.
- Paste the entire content of your JSON key file into the value field.
- What this does: This allows the GitHub Action ("the robot") to log in to your Google Cloud account securely without exposing your password in the code.

## Usage & Architecture

The pipeline is designed to run automatically ("set and forget").

**Automated Workflow**

The workflow is defined in ```.github/workflows/pipeline.yml.```

- Trigger: Wakes up hourly (e.g., at minute 37) to avoid peak traffic.
- Extract: The Python script fetches live station status and information from the API.
- Transform: Data types are cleaned, and timestamps are normalized to ensure consistent hourly reporting.
- Load: The processed dataframe is appended to the BigQuery table bike_data.status_history.

**Running Locally (Optional)**

If you want to test the script on your machine:

- Place your ```gcp_key.json``` file in the project folder.
- Run the script:
```
python main.py
```

## Example Analysis (SQL)

To move beyond simple averages, I used custom SQL to categorize stations based on their failure frequency. This query segments the network to identify "Zombie" stations (inactive units) versus those that are critically failing but operational.

Query:
```
SELECT
  CASE
    WHEN stockout_rate = 1.0 THEN '100% (Inactive)'
    WHEN stockout_rate >= 0.9 THEN '90% - 99% (Critical)'
    WHEN stockout_rate >= 0.8 THEN '80% - 90%'
    ELSE '0% - 70% (Healthy)'
  END as reliability_bucket,
  COUNT(*) as station_count
FROM (
  SELECT
    name,
    AVG(CASE WHEN num_bikes_available = 0 THEN 1.0 ELSE 0.0 END) as stockout_rate
  FROM
    `toronto-bikeshare-analytics.bike_data.status_history`
  GROUP BY
    name
)
GROUP BY 1
ORDER BY 1
```

## Results & Impact

- Operational Insight: Identified that ~8% of the network consists of inactive "Zombie Stations."
- Reliability Targeting: Pinpointed the Top 10 active stations with the highest failure rates, providing a prioritized list for rebalancing teams.
- Zero Cost: Leveraged cloud free tiers to deliver an enterprise-grade pipeline for $0.00/month.

## License

- This project is open source and available under the MIT License.

## Acknowledgments

- Data provided by the Toronto Parking Authority via the Open Data Portal.
- Built using the global GBFS (General Bikeshare Feed Specification) standard.
