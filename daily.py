import requests
import os
import base64
import json
from dotenv import load_dotenv
from google.cloud import storage

load_dotenv()

API_KEY = os.getenv("WT_API")
print(API_KEY)
ENCODED_API_KEY = base64.b64encode(API_KEY.encode()).decode()
headers = {
            'Authorization': f'Basic {ENCODED_API_KEY}'}

def create_storage_client():
    return storage.Client.from_service_account_json('wakatime-stats-cfdbfc55ee00.json')

def upload_gcp(json_data):
    destination_blob_name = f'daily-logs/{json_data}'
    # storage_client = create_storage_client()
    storage_client = storage.Client() # For github actions
    bucket = storage_client.bucket('wakatime-data')
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(json_data)
    print(f"File {json_data} uploaded to {destination_blob_name} in bucket daily-logs.")


def get_daily_stats():
    
    params = {
            # 'date': date
        }
    response = requests.get('https://wakatime.com/api/v1/users/current/status_bar/today', headers=headers, params=params)
   
    #print(response.status_code)
    #print(response.json())
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            total_seconds = data['data']['grand_total']['total_seconds']
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            date = data['data']['range']['date']
            print(f"Total coding time on {date}: {hours} hours {minutes} minutes")
            
            with open(f'coding_stats_{date}.json', 'w') as f:
                json.dump(data, f)
                print("Data saved to coding_stats.json")
            upload_gcp(f'coding_stats_{date}.json')
            print("Data uploaded to coding_stats.json")
        else:
            print("No coding data found for the given date.")
    else:
        print("Failed to retrive coding stats.")

get_daily_stats()
