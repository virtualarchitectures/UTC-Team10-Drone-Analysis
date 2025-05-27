import os
import requests
from dotenv import load_dotenv

from rich import print
import json

def download_places(place_type, radius, output_folder, api_key):
    # Load environment variables from .env file
    load_dotenv()

    # Define the endpoint URL
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    # Set up parameters for the request
    params = {
        'location': '53.34482,-6.26116',  # Fixed coordinates
        'radius': radius,                 # Parameterized radius
        'type': place_type,               # Parameterized type
        'key': api_key
    }

    file_path = os.path.join(output_folder, f'{place_type}s.json')

    # Make sure the 'data' folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Make the request to the Google endpoint
    response = requests.get(endpoint_url, params=params)

    if response.status_code == 200:
        place_data = response.json()

        # Write the JSON data to the file
        with open(file_path, 'w') as file:
            json.dump(place_data, file, indent=4)

        print(f"Data written to {file_path}")
    else:
        print(f"Request failed with status code {response.status_code}")

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')

    output_folder = 'data/locations'
    place_type = 'hospital'
    radius = 5000

    download_places(place_type, radius, output_folder, api_key)