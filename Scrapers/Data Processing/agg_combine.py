import json

def combine_dictionaries(dict1_file, dict2_file, output_file):
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