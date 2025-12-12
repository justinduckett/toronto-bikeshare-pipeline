import requests
import pandas as pd
import pandas_gbq
from datetime import datetime
from google.oauth2 import service_account
import os

# --- CONFIGURATION ---
PROJECT_ID = "toronto-bikeshare-analytics" 
DATASET_ID = "bike_data"
TABLE_ID = "status_history"

def run_pipeline():
    # 1. Fetch "Status" (Dynamic: How many bikes?)
    print("Fetching station status...")
    status_url = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status.json"
    status_resp = requests.get(status_url).json()
    status_df = pd.DataFrame(status_resp['data']['stations'])
    
    # 2. Fetch "Information" (Static: Where is it?)
    print("Fetching station info...")
    info_url = "https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information.json"
    info_resp = requests.get(info_url).json()
    info_df = pd.DataFrame(info_resp['data']['stations'])
    
    # 3. Merge them together (Enrichment)
    # We join on 'station_id' to add Name, Lat, and Lon to our counts
    print("Merging data...")
    # Keep only the columns we need from the info file
    info_clean = info_df[['station_id', 'name', 'lat', 'lon']]
    
    # Merge: effectively SQL LEFT JOIN
    final_df = status_df.merge(info_clean, on='station_id', how='left')
    
    # 4. Add Timestamp & Clean Types
    now = datetime.now()
    final_df['snapshot_time'] = now.replace(minute=0, second=0, microsecond=0)
    final_df['station_id'] = final_df['station_id'].astype(str)
    final_df['num_bikes_available'] = final_df['num_bikes_available'].astype(int)
    final_df['num_docks_available'] = final_df['num_docks_available'].astype(int)
    final_df['lat'] = final_df['lat'].astype(float)
    final_df['lon'] = final_df['lon'].astype(float)

    # 5. Authenticate & Upload
    if os.path.exists("gcp_key.json"):
        credentials = service_account.Credentials.from_service_account_file("gcp_key.json")
    else:
        print("Using GitHub Secrets...")
        import json
        key_info = json.loads(os.environ["GCP_SERVICE_ACCOUNT_KEY"])
        credentials = service_account.Credentials.from_service_account_info(key_info)

    print("Uploading to BigQuery...")
    # We stick to the same table. BigQuery handles the new columns automatically!
    pandas_gbq.to_gbq(final_df, destination_table=f"{DATASET_ID}.{TABLE_ID}", 
              project_id=PROJECT_ID, 
              if_exists='append',
              credentials=credentials)
    
    print(f"Success! Uploaded {len(final_df)} rows with Location Data.")

if __name__ == "__main__":

    run_pipeline()
