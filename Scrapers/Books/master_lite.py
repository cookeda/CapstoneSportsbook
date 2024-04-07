import json

def read_json_file(file_path):
    """Reads a JSON file and returns its contents as a dictionary."""
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json_file(data, file_path):
    """Writes a dictionary to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def combine_json_files(file_paths):
    """Combines data from multiple JSON files into a single dictionary."""
    combined_data = {}
    for file_path in file_paths:
        data = read_json_file(file_path)
        combined_data.update(data)  # This line might need adjustment based on how you want to handle key conflicts.
    return combined_data

# Define the paths to your files.
file_paths = [
    '../../Scrapers/Data/DK/CBB_Lite.json',
    '../../Scrapers/Data/DK/NBA_Lite.json',
    '../../Scrapers/Data/DK/MLB_Lite.json'
]

# Combine the data from all files.
combined_data = combine_json_files(file_paths)

# Write the combined data to a new master file.
write_json_file(combined_data, '../../DegenBets/Data/Master/matchups.json')
