import json

# Creates matchup list input that the app uses.

def read_json_file(file_path):
    """
    Reads a JSON file and returns its contents as a dictionary.

    Parameters:
    file_path (str): The path to the JSON file to be read.

    Returns:
    dict: The contents of the JSON file as a dictionary.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(data, file_path):
    """
    Writes a dictionary to a JSON file.

    This function takes a dictionary and writes it to a specified JSON file. It ensures that the JSON data is formatted
    with an indentation of 4 spaces, making it more readable.

    Parameters:
    data (dict): The dictionary containing the data to be written to the JSON file.
    file_path (str): The path to the JSON file where the data will be written. If the file does not exist, it will be created.
                     If it does exist, its contents will be overwritten with the new data.

    Returns:
    None
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def combine_json_files(file_paths):
    """
    Combines data from multiple JSON files into a single dictionary.

    This function reads each JSON file specified in the file_paths list, combines their contents into a single dictionary,
    and returns it. If multiple files contain the same keys, the value from the last file read will overwrite previous values.
    This behavior might need adjustment based on specific requirements for handling key conflicts.

    Parameters:
    file_paths (list of str): A list of strings, where each string is a path to a JSON file to be combined.

    Returns:
    dict: A dictionary containing the combined data from all specified JSON files.
    """
    combined_data = {}
    for file_path in file_paths:
        data = read_json_file(file_path)
        combined_data.update(data)  # This line might need adjustment based on how you want to handle key conflicts.
    return combined_data

# Define the paths to your files.
file_paths = [ 
    '../Data/DK/NBA_Lite.json',
    '../Data/DK/MLB_Lite.json'
]

# Combine the data from all files.
combined_data = combine_json_files(file_paths)

# Write the combined data to a new master file.
write_json_file(combined_data, '../../DegenBets/Data/Master/matchups.json')
