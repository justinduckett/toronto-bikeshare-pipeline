# Toronto Bike Share: Serverless Analytics Engineering Pipeline

This repository hosts a fully automated, serverless data pipeline that captures and analyzes real-time transit data from the Toronto Parking Authority.

It demonstrates a modern Analytics Engineering workflow: ingesting live API data via Python, warehousing it in Google BigQuery, and using Google Cloud Dataform to transform raw records into clean, business-ready data models.

View the Live Dashboard: <a href="https://lookerstudio.google.com/reporting/ee66c00f-c017-4a8d-9249-72a67b1ba3a6" target="_blank">Link to Looker Studio Report</a>

## Data Architecture & Framework

This pipeline is built on the modern ELT (Extract, Load, Transform) paradigm. It maps directly onto the five core components of modern data infrastructure:

1\. Data Sources

- Real-time transit data provided by the Toronto Parking Authority via a public REST API. The data arrives as semi-structured JSON payloads.

2\. Data Ingestion

- A Python script authenticates with the API, extracts the live JSON data, converts it into tabular formats using Pandas, and batch-loads it into the cloud.

3\. Cloud Storage (Data Warehouse)

- Google BigQuery acts as our central data warehouse. The Python script lands the raw, untouched data into a staging dataset, preserving a complete historical record of the city's bike network.
  4\. Data Transformation

- Google Cloud Dataform acts as our modeling layer. Using version-controlled SQL (.sqlx), Dataform cleans the raw BigQuery tables by removing duplicates and handling missing values. It also models the data into clean tables ready for business analysis.

5\. Orchestration & Scheduling

- Rather than deploying a complex orchestrator like Airflow, this project utilizes a lightweight, serverless scheduling approach:
  - GitHub Actions runs a cron job every 4 hours to execute the Python ingestion script.
  - Dataform’s built-in scheduler runs independently to update the transformation models once the new data has landed.

## Tech Stack

- **Python (Requests, Pandas):** Handles data ingestion by authenticating with the API, extracting live JSON payloads, and converting them into structured dataframes.
- **GitHub Actions:** Acts as a lightweight, serverless scheduler that automatically triggers the Python ingestion script every 4 hours.
- **Google BigQuery:** Serves as the highly scalable cloud data warehouse, acting as the centralized storage for both the raw historical data and the final analytics tables.
- **Google Cloud Dataform:** Powers the data transformation layer using version-controlled SQL (.sqlx) to clean, filter, and model the raw staging data into optimized tables.
- **Looker Studio:** Delivers the presentation layer, connecting directly to BigQuery to visualize the clean data via interactive dashboards and spatial maps.

## Core Data Models (Dataform)

Instead of writing complex SQL directly in the dashboard, we use .sqlx files in Dataform to create modular, reusable tables:

- active_fleet_size: Tracks the total number of bikes available across the city over time.
- network_health_histogram: Identifies "Zombie Stations" that remain empty for long periods, highlighting rebalancing challenges.
- map_colour_grouping: Prepares geographic data for high-performance mapping in Looker Studio.

## Key Features

- 100% Serverless & Cost-Optimized: Built entirely on cloud-native, free-tier resources. Infrastructure scales automatically with zero upkeep costs.
- Software Engineering Best Practices: Transformation logic is fully version-controlled in Git. Changes can be audited, reviewed, and safely rolled back if necessary.
- Automated Quality Checks: The pipeline is designed to exclude "bad data" (like duplicate rows or blank station names) before it hits the dashboard.

## Acknowledgments & License

- Data provided by the Toronto Parking Authority via the Toronto Open Data Portal.
- Built utilizing the global GBFS (General Bikeshare Feed Specification) standard framework.
- This project is open-source and available under the MIT License.
