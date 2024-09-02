import os
import json
import pandas as pd
from datetime import datetime

with open('config/sample-cities.json','r') as f:
    config = json.load(f)

def fetch_unique_data(directory : str):
    """
    Upload all unique data checking for each city the date on which the weather conditions were detected thus avoiding data duplication
    
    returns:\n
    unique_files -> list:
        The number of unique files found
    num_total_files -> int:
        The total number of files fetched

    return (unique_files, num_total_files)
    """
    sample_cities = config['sample-cities']
    reports = os.listdir(directory)
    seen_dates = set()
    num_total_files = len(sample_cities) * len(reports)
    num_unique_files = 0

    for city in sample_cities:
        for report in reports:
            if not os.path.exists(f'{directory}/{report}/{city}.json'):
                num_total_files -= 1
                continue

            with open(f'{directory}/{report}/{city}.json', 'r') as f:
                content = json.load(f,parse_int=True,parse_float=True)

            local_obs_time = content["current_condition"][0]["localObsDateTime"]

            if local_obs_time not in seen_dates:
                seen_dates.add(local_obs_time)
                num_unique_files+=1

                useful_data = content['current_condition'][0]
                useful_data['area'] = content['nearest_area'][0]['areaName'][0]['value']
                useful_data['country'] = content['nearest_area'][0]['country'][0]['value']
                useful_data['latitude'] = content['nearest_area'][0]['latitude']
                useful_data['longitude'] = content['nearest_area'][0]['longitude']
                useful_data['population'] = content['nearest_area'][0]['population']
                useful_data['region'] = content['nearest_area'][0]['region'][0]['value']
                useful_data['weatherDesc'] = content['current_condition'][0]['weatherDesc'][0]['value']

                useful_data['localObsDateTime'] = datetime.strptime(useful_data['localObsDateTime'], '%Y-%m-%d %I:%M %p')
                useful_data['minute'] = useful_data['localObsDateTime'].minute
                useful_data['hour'] = useful_data['localObsDateTime'].hour
                useful_data['day'] = useful_data['localObsDateTime'].day
                useful_data['month'] = useful_data['localObsDateTime'].month
                useful_data['year'] = useful_data['localObsDateTime'].year

                useful_data.pop("observation_time")
                useful_data.pop("weatherIconUrl")

                yield useful_data
            else:
                num_total_files -= 1
                os.remove(f'{directory}/{report}/{city}.json')
                pass
                #print(f"Duplicate reports for city: {city} at: {local_obs_time}")

        seen_dates = set()
    print(f"Unique Files: {num_unique_files}; Total Files: {num_total_files}; Percentage: {(num_unique_files / (num_total_files)) * 100:.2f}%")

#fetch_unique_data('data/collected')