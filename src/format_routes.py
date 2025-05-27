import os
import json

def convert_format(input_data):
    # Extract the relevant information and convert
    formatted_data = [
        {
            "longitude": entry["location"]["lng"],
            "latitude": entry["location"]["lat"],
            "height": (entry["elevation"])
        }
        for entry in input_data["results"]
    ]
    return formatted_data

def process_files(input_directory, output_directory):
    # List all JSON files in the input directory
    for file_name in os.listdir(input_directory):
        if file_name.endswith(".json"):
            input_path = os.path.join(input_directory, file_name)
            output_path = os.path.join(output_directory, file_name)

            # Read the input JSON file
            with open(input_path, 'r') as input_file:
                input_data = json.load(input_file)
            
            # Convert the data format
            formatted_data = convert_format(input_data)
            
            # Write the output JSON file
            with open(output_path, 'w') as output_file:
                json.dump(formatted_data, output_file, indent=2)

if __name__ == "__main__":
    input_directory = "data/elevated_routes"
    output_directory = "data/formatted_routes"
    
    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)
    
    # Process files
    process_files(input_directory, output_directory)