import json

def combine_dictionaries(dict1_file, dict2_file, output_file):
    """
    Combines two dictionaries from separate JSON files and saves the combined dictionary to a new JSON file.

    Parameters:
    dict1_file (str): The path to the first dictionary JSON file.
    dict2_file (str): The path to the second dictionary JSON file.
    output_file (str): The path to the output JSON file where the combined dictionary will be saved.

    Returns:
    None. The combined dictionary is saved to the output file.

    Raises:
    FileNotFoundError: If either of the input files or the output file does not exist.
    ValueError: If either of the input files is not a valid JSON file.
    """
    # Load dictionaries from files
    with open(dict1_file, 'r', encoding='utf-8') as file1:
        dict1 = json.load(file1)

    with open(dict2_file, 'r', encoding='utf-8') as file2:
        dict2 = json.load(file2)

    # Combine the dictionaries
    combined_dict = {**dict1, **dict2}

    # Save the combined dictionary to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(combined_dict, file, ensure_ascii=False, indent=4)

# Usage
combine_dictionaries('Clean/NBA/Aggregate.json', 'Clean/MLB/Aggregate.json', '../../DegenBets/Data/Cleaned/AggregateOdds.json')