import json
import sys

# Command-line input handling
if len(sys.argv) < 2:
    print("Usage: python aggregate_odds.py <LEAGUE_NAME>")
    sys.exit(1)

league = sys.argv[1]
input_files = [f'../Data/Bovada/{league}.json', f'../Data/DK/{league}.json', f'../Data/ESPN/{league}.json']
# f'../Data/ESPN/{league}.json',
output_file = f'Clean/{league}/Aggregate.json'

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def aggregate_files(input_files, output_file):
    """
    Aggregates odds data from multiple input JSON files and writes the aggregated data to an output JSON file.

    Parameters:
    input_files (list): A list of input file paths containing odds data in JSON format.
    output_file (str): The path of the output JSON file where the aggregated odds data will be written.

    Returns:
    None: This function does not return any value. It writes the aggregated odds data to the specified output file.

    Raises:
    ValueError: If the input file list is empty or if the specified output file does not exist.

    Usage:
    To use this function, provide a list of input file paths and the desired output file path. The function will aggregate the odds data from the input files and write the aggregated data to the specified output file.

    Example:
    input_files = ['../Data/Bovada/league.json', '../Data/DK/league.json', '../Data/ESPN/league.json']
    output_file = 'Clean/league/Aggregate.json'
    aggregate_files(input_files, output_file)
    """
    all_games = {}
    # Aggregate data from each book
    for file_path in input_files:
        data = load_data(file_path)
        for game_list in data:
            for game_data in game_list:
                matchup_id = game_data['MatchupID']
                if matchup_id not in all_games:
                    all_games[matchup_id] = {
                        'Info Table': game_data['Info Table'],
                        'Bet Tables': {}
                    }
                book_name = game_data['Odds Table']['Book Name']
                all_games[matchup_id]['Bet Tables'][book_name] = game_data['Odds Table']
    
    # Prepare the output data
    output_data = {}
    for game_id, game in all_games.items():
        bet_tables = []
        for book, odds in game['Bet Tables'].items():
            bet_tables.append({'Book Name': book, **odds})
        output_data[game_id] = {
            'Info Table': game['Info Table'],
            'Bet Tables': bet_tables
        }


    # Write the aggregated odds to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, indent=4, ensure_ascii=False)

# Execute the aggregation function
aggregate_files(input_files, output_file)
