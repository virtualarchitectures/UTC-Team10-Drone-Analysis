import os
import requests
from dotenv import load_dotenv

from rich import print
from rich.console import Console
from rich.table import Table
import json

def get_path_elevation(path, samples=10, api_key):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/elevation/json",
        params={
            "path": path,
            "samples": samples,
            "key": api_key
        }
    )
    result = response.json()
    return result['results'] if result['results'] else []

def save_route_to_file(route, filename):
    with open(filename, 'w') as file:
        json.dump(route, file, indent=4)

def load_hospitals(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['results']

def generate_route_file(origin, destination, api_key, pair_index):
    path = f"{origin['lat']},{origin['lng']}|{destination['lat']},{destination['lng']}"
    elevations = get_path_elevation(path, api_key=api_key)
    route = {
        "results": elevations,
        "status": "OK"
    }
    # Save each path to its own file
    filename = f"data/elevated_route_{pair_index}.json"
    save_route_to_file(route, filename)

def generate_routes(hospitals, api_key):
    for i, origin in enumerate(hospitals):
        for j, destination in enumerate(hospitals):
            if i != j:  # Avoid using the same hospital as origin and destination
                generate_route_file(origin['geometry']['location'], destination['geometry']['location'], api_key, f"{i}_{j}")

def main():
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    hospitals = load_hospitals('data/hospitals.json')
    generate_routes(hospitals, api_key)

if __name__ == "__main__":
    main()
