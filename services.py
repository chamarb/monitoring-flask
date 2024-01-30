from pysnmp.hlapi import *
import requests
from datetime import datetime, timedelta

def get(target, community, oid):
    ErrorIndication, ErrorStatus, ErrorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((target, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))
               )
    )
    if ErrorIndication:
        return f'Error Indication {ErrorIndication}'
    if ErrorStatus:
        return f'Error Status {ErrorStatus}'
    return varBinds[0][1]

def perform_prediction(city_name, api_key):
    # Fetch historical precipitation data from OpenWeatherMap API
    base_url = "http://api.openweathermap.org/data/2.5/onecall/timemachine"
    
    # Calculate the start and end timestamps for the last 7 days
    start_timestamp = int((datetime.now() - timedelta(days=7)).timestamp())
    end_timestamp = int(datetime.now().timestamp())

    params = {
        'q': city_name,
        'appid': api_key,
        'start': start_timestamp,
        'end': end_timestamp
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        return f'Error fetching data from OpenWeatherMap API. Status code: {response.status_code}'

    data = response.json()

    # Extract relevant precipitation data from the API response
    precipitation_data = [entry.get('precipitation', 0) for entry in data.get('hourly', [])]

    # Perform predictions using a simple logic (average precipitation)
    average_precipitation = sum(precipitation_data) / len(precipitation_data)

    # Return the prediction results
    prediction_results = {'city': city_name, 'average_precipitation': average_precipitation}





ip_target = '127.0.0.1'
community = 'public'
memory_storage_oid = '1.3.6.1.2.1.25.2.3.1.5.1'
memory_used_oid = '1.3.6.1.2.1.25.2.3.1.6.1'

if __name__ == '__main__':
    print('memory storage', get(ip_target, community, memory_storage_oid))
    print('used memory', get(ip_target, community, memory_used_oid))
