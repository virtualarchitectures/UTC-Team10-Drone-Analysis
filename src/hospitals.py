import os
import requests
from dotenv import load_dotenv

from rich import print
from rich.console import Console
from rich.table import Table
import json  # New import statement

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get the API key from the environment
    api_key = os.getenv('GOOGLE_API_KEY')

    if not api_key:
        raise ValueError("API key not set in .env file")

    # Define the endpoint URL
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    # Set up parameters for the request
    params = {
        'location': '53.34482,-6.26116',  # Updated coordinates
        'radius': 5000,                   # Updated radius
        'type': 'hospital',
        'key': api_key
    }

    # Define the data folder and file path
    output_folder = 'data/locations'
    file_path = os.path.join(output_folder, 'hospitals.json')

    # Make sure the 'data' folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Make the request to the Google endpoint
    response = requests.get(endpoint_url, params=params)

    if response.status_code == 200:
        hospitals_data = response.json()

        # Write the JSON data to the file
        with open(file_path, 'w') as file:
            json.dump(hospitals_data, file, indent=4)

        print(f"Data written to {file_path}")
    else:
        print(f"Request failed with status code {response.status_code}")

if __name__ == "__main__":
    main()
