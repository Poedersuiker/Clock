import requests
import json


def fetch_json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.json()  # Parse JSON response
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)


url = 'https://api.openweathermap.org/data/2.5/forecast?lat=52.04&lon=5.67&units=metric&appid=b959aff47fc0058e7d8e3a6b3c0b558e'
json_data = fetch_json_data(url)

print(json_data)
