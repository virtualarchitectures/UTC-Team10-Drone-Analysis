import os
import requests
from dotenv import load_dotenv

from rich import print
from rich.console import Console
from rich.table import Table
import json
import re

def clean_name(name):
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\bThe\b', '', name)
    name = name.strip()
    name_parts = name.split()
    cleaned_name = "_".join(name_parts[:2])
    return cleaned_name

def get_path_elevation(path, api_key, samples=10):
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
    path = f"{origin['geometry']['location']['lat']},{origin['geometry']['location']['lng']}|{destination['geometry']['location']['lat']},{destination['geometry']['location']['lng']}"
    elevations = get_path_elevation(path, api_key=api_key, samples=10)
    route = {
        "results": elevations,
        "status": "OK"
    }
    origin_name = clean_name(origin['name'])
    destination_name = clean_name(destination['name'])
    filename = f"data/{pair_index}_{origin_name}_to_{destination_name}.json"
    save_route_to_file(route, filename)

def generate_routes(hospitals, api_key):
    for i, origin in enumerate(hospitals):
        for j, destination in enumerate(hospitals):
            if i != j:  # Avoid using the same hospital as origin and destination
                generate_route_file(origin, destination, api_key=api_key, pair_index=f"{i}_{j}")

def main():
    load_dotenv()
    api_key = os.getenv('GOOGLE_API_KEY')
    hospitals = load_hospitals('data/hospitals.json')
    generate_routes(hospitals, api_key)

if __name__ == "__main__":
    main()
