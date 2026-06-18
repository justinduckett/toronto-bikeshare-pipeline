# Toronto Bike Share: Serverless Analytics Engineering Pipeline

This repository hosts a fully automated, serverless data pipeline that captures and analyzes real-time transit data from the Toronto Parking Authority.

It demonstrates a modern Analytics Engineering workflow: ingesting live API data via Python, warehousing it in Google BigQuery, and using Google Cloud Dataform to transform raw records into clean, business-ready data models.

View the Live Dashboard: <a href="https://lookerstudio.google.com/reporting/ee66c00f-c017-4a8d-9249-72a67b1ba3a6" target="_blank">Link to Looker Studio Report</a>

## Data Architecture & Framework

This pipeline is built on the modern ELT (Extract, Load, Transform) paradigm. It maps directly onto the five core components of modern data infrastructure:

1\. Data Sources

- Real-time transit data provided by the Toronto Parking Authority via a public REST API. The data arrives as semi-structured JSON payloads.

2\. Data Ingestion

- A custom Python script extracts the live JSON data and formats it into Pandas dataframes. The code is version-controlled in GitHub, but execution is handled serverlessly by Google Cloud Run Functions. This provides a highly reliable, zero-maintenance cloud environment that eliminates third-party queue wait times.

3\. Cloud Storage (Data Warehouse)

- Google BigQuery acts as our central data warehouse. The Python script lands the raw, untouched data into a staging dataset, preserving a complete historical record of the city's bike network.
  4\. Data Transformation

- Google Cloud Dataform acts as our modeling layer. Using version-controlled SQL (.sqlx), Dataform cleans the raw BigQuery tables by removing duplicates and handling missing values. It also models the data into clean tables ready for business analysis.

5\. Orchestration & Scheduling

- A 100% serverless, Google-native scheduling architecture:
  - Google Cloud Scheduler strictly enforces a 4-hour cron SLA to wake up and trigger the Cloud Run Function ingestion.

  - Dataform’s native scheduler runs the SQL transformations immediately after, ensuring the dashboard is always powered by fresh, modeled data.

## Tech Stack

- **Python (Requests, Pandas):** Handles data ingestion by authenticating with the API, extracting live JSON payloads, and converting them into structured dataframes.
- **Google Cloud Run Functions:** Acts as the serverless compute engine, providing a reliable, scalable environment for the Python ingestion logic.
- **Google Cloud Scheduler:** The centralized "alarm clock" that triggers the ingestion pipeline on a precise 4-hour cadence.
- **Google BigQuery:** Serves as the highly scalable cloud data warehouse, acting as the centralized storage for both the raw historical data and the final analytics tables.
- **Google Cloud Dataform:** Powers the data transformation layer using version-controlled SQL (.sqlx) to clean, filter, and model the raw staging data into optimized tables.
- **Looker Studio:** Delivers the presentation layer, connecting directly to BigQuery to visualize the clean data via interactive dashboards and spatial maps.

## Core Data Models (Dataform)

Instead of writing complex SQL directly in the dashboard, we use .sqlx files in Dataform to create modular, reusable tables:

- `active_fleet_size`: Tracks the total number of bikes available across the city over time.
- `network_health_histogram`: Identifies "Zombie Stations" that remain empty for long periods, highlighting rebalancing challenges.
- `map_colour_grouping`: Prepares geographic data for high-performance mapping in Looker Studio.

## Key Features

- 100% Serverless & Cost-Optimized: Built entirely on cloud-native, free-tier resources. Infrastructure scales automatically with zero upkeep costs.
- Software Engineering Best Practices: Transformation logic is fully version-controlled in Git. Changes can be audited, reviewed, and safely rolled back if necessary.
- Automated Quality Checks: The pipeline is designed to exclude "bad data" (like duplicate rows or blank station names) before it hits the dashboard.

## Acknowledgments & License

- Data provided by the Toronto Parking Authority via the Toronto Open Data Portal.
- Built utilizing the global GBFS (General Bikeshare Feed Specification) standard framework.
- This project is open-source and available under the MIT License.
