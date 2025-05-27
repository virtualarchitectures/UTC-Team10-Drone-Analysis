import os
import requests
from dotenv import load_dotenv

from rich import print
from rich.console import Console
from rich.table import Table
import json

# TODO: Use the path API and pipe the locations to test
# https://maps.googleapis.com/maps/api/elevation/json?path=53.3601,-6.2652%7C53.3346,-6.2885&samples=15&key=
# Set samples to 10
# Output a separate file for each origin and destination pair
def get_elevation(location, api_key):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/elevation/json",
        params={
            "locations": f"{location['lat']},{location['lng']}",
            "key": api_key
        }
    )
    result = response.json()
    return result['results'][0]['elevation'] if result['results'] else None
def load_hospitals(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['results']

def generate_route(hospitals, api_key):
    route = []
    for hospital in hospitals:
        location = hospital['geometry']['location']
        elevation = get_elevation(location, api_key)
        route.append({
            "elevation": elevation,
            "location": location,
            "resolution": 4.771975994110107
        })
    return {"results": route, "status": "OK"}

def save_route_to_file(route, filename):
    with open(filename, 'w') as file:
        json.dump(route, file, indent=4)

def main():
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    hospitals = load_hospitals('data/hospitals.json')
    route = generate_route(hospitals, api_key)
    save_route_to_file(route, 'data/elevated_routes.json')

if __name__ == "__main__":
    main()
