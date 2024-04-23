import json
import sys

# Command-line input handling
if len(sys.argv) < 2:
    print("Usage: python aggregate_odds.py <LEAGUE_NAME>")
    sys.exit(1)

league = sys.argv[1]
input_files = [f'../Data/ESPN/{league}.json', f'../Data/Bovada/{league}.json', f'../Data/DK/{league}.json']
output_file = f'Clean/{league}/Aggregate.json'

def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def aggregate_files(input_files, output_file):
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
    output_data = []
    for game_id, game in all_games.items():
        bet_tables = []
        for book, odds in game['Bet Tables'].items():
            bet_tables.append({'Book Name': book, **odds})
        output_data.append({
            'MatchupID': game_id,
            'Info Table': game['Info Table'],
            'Bet Tables': bet_tables
        })

    # Write the aggregated odds to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, indent=4, ensure_ascii=False)

# Execute the aggregation function
aggregate_files(input_files, output_file)
