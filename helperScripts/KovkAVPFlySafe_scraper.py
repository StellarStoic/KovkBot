import requests
import json

def fetch_weather_data(api_url, entries_count=18):
    # Send a GET request to the API
    response = requests.get(api_url)

    # Check if the response is successful
    if response.status_code != 200:
        print("Failed to retrieve data from API.")
        return [], [], [], [], []

    # Load JSON data from the response
    data = json.loads(response.text)
    
    # Limit the data to the last 'entries_count' entries
    data = data[-entries_count:] # Remove entries_count=18 to use more data


    # Initialize lists to store weather data
    time_data = []
    wind_speed = []
    wind_gusts = []
    wind_direction = []
    temperature = []

    # Extracting required data from each record in the JSON data
    for record in data:
        # Extract and format time
        time_str = record.get("ts", "").split()[-1][:-3]  # Extracting time and removing seconds
        time_data.append(time_str)

        # Extract wind speed, gusts, direction, and temperature
        wind_speed.append(float(record.get("wind_avg", 0)))
        wind_gusts.append(float(record.get("wind_gust", 0)))
        wind_direction.append(int(record.get("wind_d", 0)))
        temperature.append(int(record.get("temp", 0)))

    return time_data, wind_speed, wind_gusts, wind_direction, temperature

# URL of the new API
api_url = 'https://flysafe.pro/api/kovk'

# Fetch and print the weather data
time, speed, gusts, direction, temp = fetch_weather_data(api_url)
print("Time:", time)
print("Wind Speed:", speed)
print("Wind Gusts:", gusts)
print("Wind Direction:", direction)
print("Temperature:", temp)
