import requests
import pandas as pd
import pandas_gbq

# --- CONFIGURATION ---
PROJECT_ID = "toronto-bikeshare-analytics"
DATASET_ID = "bike_data"
TABLE_ID = "status_history"


def main(request):
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
    print("Merging data...")
    info_clean = info_df[['station_id', 'name', 'lat', 'lon']]
    final_df = status_df.merge(info_clean, on='station_id', how='left')

    # 4. Add Timestamp & Clean Types
    # Store the feed's own report time as a clean UTC instant.
    # All local time conversion happens later, in SQL.
    final_df['snapshot_time'] = pd.to_datetime(status_resp['last_updated'], unit='s', utc=True)

    final_df['station_id'] = final_df['station_id'].astype(str)
    final_df['num_bikes_available'] = final_df['num_bikes_available'].astype(int)
    final_df['num_docks_available'] = final_df['num_docks_available'].astype(int)
    final_df['lat'] = final_df['lat'].astype(float)
    final_df['lon'] = final_df['lon'].astype(float)

    # 5. Authenticate & Upload
    print("Uploading to BigQuery...")
    pandas_gbq.to_gbq(final_df, destination_table=f"{DATASET_ID}.{TABLE_ID}",
                      project_id=PROJECT_ID,
                      if_exists='append')

    print(f"Success! Uploaded {len(final_df)} rows with Location Data.")
    return "Pipeline executed successfully!"
