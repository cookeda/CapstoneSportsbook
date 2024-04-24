import json
import sys

# Define the input files and output file paths
if len(sys.argv) < 2:
    print("Usage: python league_best_odds.py <LEAGUE_NAME>")
    sys.exit(1)

league = sys.argv[1].upper()

input_files = [f'../Data/ESPN/{league}.json', f'../Data/Bovada/{league}.json', f'../Data/DK/{league}.json']
output_file = f'Clean/{league}/Best.json'

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

                odds_table = game_data['Odds Table']
                book_name = odds_table['Book Name']
                # Handle Spread
                spread_line = normalize_odd(odds_table['Away Spread'])
                spread_odds = normalize_odd(odds_table['Away Spread Odds'])
                spread_key = 'Best Spread'
                if spread_key not in all_games[matchup_id]['Odds Table'] or \
                   spread_line > all_games[matchup_id]['Odds Table'][spread_key]['line']:
                    all_games[matchup_id]['Odds Table'][spread_key] = {
                        'line': spread_line,
                        'odds': spread_odds,
                        'book': book_name
                    }

                # Handle Total
                total_points = normalize_odd(odds_table['Total Points'])
                over_odds = normalize_odd(odds_table['Over Odds'])
                under_odds = normalize_odd(odds_table['Under Odds'])
                total_key = 'Best Total'
                if total_key not in all_games[matchup_id]['Odds Table'] or \
                   total_points < all_games[matchup_id]['Odds Table'][total_key]['line']:  # Assuming you want the lowest total for best 'under' bet
                    all_games[matchup_id]['Odds Table'][total_key] = {
                        'line': total_points,
                        'over_odds': over_odds,
                        'under_odds': under_odds,
                        'book': book_name
                    }

    # Prepare data for output
    output_data = []
    for game_id, game in all_games.items():
        game_odds = {
            'Best Spread': f"{game['Odds Table']['Best Spread']['line']} at odds {game['Odds Table']['Best Spread']['odds']} ({game['Odds Table']['Best Spread']['book']})",
            'Best Total': f"{game['Odds Table']['Best Total']['line']} (Over odds: {game['Odds Table']['Best Total']['over_odds']}, Under odds: {game['Odds Table']['Best Total']['under_odds']}) ({game['Odds Table']['Best Total']['book']})"
        }
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

