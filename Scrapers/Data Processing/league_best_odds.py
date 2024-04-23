import json
import sys 

# Define the input files and output file paths
if len(sys.argv) < 2:
    print("Usage: python league_best_odds.py <LEAGUE_NAME>")
    sys.exit(1)

league = sys.argv[1].upper()

input_files = [f'../Data/Bovada/{league}.json', f'../Data/DK/{league}.json', f'../Data/ESPN/{league}.json']
output_file = f'Clean/Best_{league}.json'

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def normalize_odd(odd):
    """ Normalize the odds to handle Unicode minus sign and convert to float. """
    return float(odd.replace('−', '-'))

def process_files(input_files, output_file):
    all_games = {}
    # Load and process each file
    for file_path in input_files:
        data = load_data(file_path)
        for game_list in data:
            for game_data in game_list:
                matchup_id = game_data['MatchupID']
                if matchup_id not in all_games:
                    all_games[matchup_id] = {
                        'Info Table': game_data['Info Table'],
                        'Odds Table': {}
                    }
                # Update the best odds
                odds_table = game_data['Odds Table']
                book_name = odds_table['Book Name']
                for key, value in odds_table.items():
                    if key != 'Book Name':
                        if (key not in all_games[matchup_id]['Odds Table'] or
                                normalize_odd(value) < normalize_odd(all_games[matchup_id]['Odds Table'][key][0])):
                            all_games[matchup_id]['Odds Table'][key] = (value, book_name)
    
    # Prepare data for output
    output_data = []
    for game_id, game in all_games.items():
        game_odds = {k: f"{v[0]} ({v[1]})" for k, v in game['Odds Table'].items()}
        output_data.append({
            'MatchupID': game_id,
            'Info Table': game['Info Table'],
            'Odds Table': game_odds
        })
    
    # Write the best odds to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, indent=4, ensure_ascii=False)

# Execute the processing function
process_files(input_files, output_file)
