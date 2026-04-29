# Toronto Bike Share: Serverless Analytics Engineering Pipeline

This repository hosts a fully automated, serverless ELT pipeline that captures real-time transit data from the Toronto Parking Authority.

It demonstrates a modern Analytics Engineering workflow: ingesting raw API data via Python, warehousing it in Google BigQuery, and using Google Cloud Dataform to transform raw records into clean, business-ready data models for visualization.

View the Live Dashboard: [Link to Looker Studio Report](https://lookerstudio.google.com/reporting/ee66c00f-c017-4a8d-9249-72a67b1ba3a6)

## How It Works

**Extract & Load (Python):** A GitHub Action runs every 4 hours to fetch live station status from the GBFS API and append it to a historical table in BigQuery.

**Transform (Dataform):** Google Cloud Dataform runs version-controlled SQL (.sqlx) to calculate fleet size, station health, and stockout rates.

**Visualize (Looker Studio):** Interactive dashboards read from the pre-calculated tables for high-performance reporting.

## Tech Stack

**Ingestion:** Python (Pandas, Requests).

**Orchestration:** GitHub Actions (Cron Scheduler).

**Warehousing:** Google BigQuery.

**Transformation:** Google Cloud Dataform (SQLx).

**Visualization:** Looker Studio.

## Key Features

**Serverless & Cost-Effective:** The entire pipeline runs on free-tier cloud resources, optimized to run every 4 hours to preserve compute credits.

**Cloud-Native Security:** Uses custom Google Cloud IAM service accounts with "least-privilege" access to secure the automated workflow.

**Version-Controlled Logic:** Transformation logic is no longer hidden in dashboard filters; it is stored in Git as code for easy tracking and "rewinding".

## Insights Delivered

**Network Reliability:** Identifies "Zombie Stations" (0 bikes available for >7 days) which make up ~8% of the network.

**Stockout Rates:** Calculates the percentage of time stations are failing users by remaining empty.

## License

This project is open-source and available under the MIT License.

## Acknowledgments

Data provided by the Toronto Parking Authority via the Open Data Portal.

Built using the global GBFS (General Bikeshare Feed Specification) standard.
