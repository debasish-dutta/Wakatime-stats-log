import requests
import os
import base64
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
ENCODED_API_KEY = base64.b64encode(API_KEY.encode()).decode()
headers = {
            'Authorization': f'Basic {ENCODED_API_KEY}'}

def get_all_stats():
    params = {

        }

    response = requests.get('https://wakatime.com/api/v1/users/current/stats/last_year', headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            with open('coding_stats_all_13_7_23.json', 'w') as f:
                json.dump(data, f)
                print("Data saved to coding_stats_all_13_7_23.json")
        else:
            print("No coding data found")
    else:
        print("Failed to retrive coding stats.")

get_all_stats()
