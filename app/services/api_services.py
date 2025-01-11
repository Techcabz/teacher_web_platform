import requests
from flask import current_app

def fetch_data_from_api(endpoint, params=None):
    api_url = current_app.config['API_URL']
    api_key = current_app.config['API_KEY']

    if not api_url or not api_key:
        raise ValueError("API URL or API Key is missing in configuration.")

    full_url = f"{api_url}/{endpoint}"
    headers = {
        'Authorization': f'Bearer {api_key}'
    }

    # Send GET request to the API with headers
    response = requests.get(full_url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        return response.json() 
    else:
        raise Exception(f"Error fetching data from API. Status code: {response.status_code}")

