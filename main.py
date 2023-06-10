import requests
import datetime
import os
import base64
import json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
ENCODED_API_KEY = base64.b64encode(API_KEY.encode()).decode()
headers = {
            'Authorization': f'Basic {ENCODED_API_KEY}'}
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
            
            with open('coding_stats_{date}.json', 'w') as f:
                json.dump(data, f)
                print("Data saved to coding_stats.json")
        else:
            print("No coding data found for the given date.")
    else:
        print("Failed to retrive coding stats.")

def get_all_stats():
    params = {

        }

    response = requests.get('https://wakatime.com/api/v1/users/current/stats/last_year', headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            with open('coding_stats_all_.json', 'w') as f:
                json.dump(data, f)
                print("Data saved to coding_stats_all_.json")
        else:
            print("No coding data found")
    else:
        print("Failed to retrive coding stats.")

today = datetime.date.today().strftime("%Y-%m-%d")

get_daily_stats()
get_all_stats()
