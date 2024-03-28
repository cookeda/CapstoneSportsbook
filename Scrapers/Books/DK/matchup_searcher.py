import os
import json


def search_across_files(folder_path, bet_table_id):
    odds_info_list = []  # Holds the results found across files

    # Walk through each subdirectory in the folder_path
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.json'):  # Check if the file is a JSON file
                file_path = os.path.join(dirpath, filename)
                
                # Open and load the JSON data
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding JSON from {file_path}: {e}")
                        continue  # Skip this file if it's not valid JSON
                    
                    # Search each matchup group in the data
                    for matchup_group in data:
                        for matchup in matchup_group:
                            if matchup.get('BetTableId') == bet_table_id:
                                odds_info_list.append(matchup['Odds Table'])

    return odds_info_list


# Example Usage
folder_path = '../../data/DK'  # Update this to your folder's path
bet_table_id_example = "DK_TWlsd2F1a2Vl_TmV3IE9ybGVhbnM=_NBA"
results = search_across_files(folder_path, bet_table_id_example)

if results:
    for odds_info in results:
        print(f"Found Odds Info: {odds_info}")
else:
    print("Bet Table ID not found in any file.")
