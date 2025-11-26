import requests
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
import os

# --- CONFIGURATION ---
PROJECT_ID = "toronto-bikeshare-analytics"
DATASET_ID = "bike_data"
TABLE_ID = "status_history"

def run_pipeline():
    # 1. Fetch Data
    url = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status.json"
    print("Fetching data...")
    response = requests.get(url)
    
    # 2. Process Data
    data = response.json()['data']['stations']
    df = pd.DataFrame(data)
    df['snapshot_time'] = datetime.now()
    
    # 3. Clean Types
    df['station_id'] = df['station_id'].astype(str)
    df['num_bikes_available'] = df['num_bikes_available'].astype(int)
    df['num_docks_available'] = df['num_docks_available'].astype(int)

    # 4. Authenticate & Upload
    # We use a special trick here to read the key from GitHub's secret vault
    # If we are local, we use the file. If on GitHub, we uses the Environment Variable.
    if os.path.exists("gcp_key.json"):
        credentials = service_account.Credentials.from_service_account_file("gcp_key.json")
    else:
        # This part runs on GitHub
        print("Using GitHub Secrets...")
        # We will set this up in the next step
        import json
        key_info = json.loads(os.environ["GCP_SERVICE_ACCOUNT_KEY"])
        credentials = service_account.Credentials.from_service_account_info(key_info)

    print("Uploading to BigQuery...")
    df.to_gbq(destination_table=f"{DATASET_ID}.{TABLE_ID}",
              project_id=PROJECT_ID,
              if_exists='append',
              credentials=credentials)
    
    print("Success! Data saved.")

if __name__ == "__main__":
    run_pipeline()