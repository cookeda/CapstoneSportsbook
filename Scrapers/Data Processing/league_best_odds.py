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
    """ Open file """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def normalize_odd(odd):
    """ Normalize the odds to handle Unicode minus sign and convert to float. """
    return float(odd.replace('−', '-'))

def process_files(input_files, output_file):
    """
    Process the input files, update the best odds, and write the best odds to the output file.

    Parameters:
    input_files (list): A list of input file paths.
    output_file (str): The output file path.

    Returns:
    None

    The function processes each input file, updates the best odds for each game, and writes the best odds to the output file.
    """
    all_games = {}  # A dictionary to store the best odds for each game.

    # Load and process each file
    for file_path in input_files:
        data = load_data(file_path)  # Load the data from the input file.
        for game_list in data:
            for game_data in game_list:
                matchup_id = game_data['MatchupID']  # Get the matchup ID from the game data.
                if matchup_id not in all_games:  # If the matchup ID is not in the all_games dictionary, add it with initial values.
                    all_games[matchup_id] = {
                        'Info Table': game_data['Info Table'],  # Add the info table to the game data.
                        'Odds Table': {}  # Initialize the odds table for the game.
                    }
                # Update the best odds
                odds_table = game_data['Odds Table']  # Get the odds table from the game data.
                book_name = odds_table['Book Name']  # Get the book name from the odds table.
                for key, value in odds_table.items():  # Iterate through the odds table.
                    if key != 'Book Name':  # Skip the book name.
                        if (key not in all_games[matchup_id]['Odds Table'] or  # Check if the key is already in the odds table.
                                normalize_odd(value) > normalize_odd(all_games[matchup_id]['Odds Table'][key][0])):  # If the value is smaller than the current best odds, update the odds table.
                            all_games[matchup_id]['Odds Table'][key] = (value, book_name)  # Update the odds table with the new best odds and book name.

    # Prepare data for output
    output_data = []  # Initialize an empty list to store the output data.
    for game_id, game in all_games.items():  # Iterate through the all_games dictionary.
        game_odds = {k: f"{v[0]} ({v[1]})" for k, v in game['Odds Table'].items()}  # Format the odds table for the output.
        output_data.append({
            'MatchupID': game_id,  # Add the matchup ID to the output data.
            'Info Table': game['Info Table'],  # Add the info table to the output data.
            'Odds Table': game_odds  # Add the formatted odds table to the output data.
        })  # Add the formatted odds table to the output data.

    # Write the best odds to the output file
    with open(output_file, 'w', encoding='utf-8') as file:  # Open the output file for writing.
        json.dump(output_data, file, indent=4, ensure_ascii=False)  # Write the output data to the output file in JSON format.
# Execute the processing function
process_files(input_files, output_file)
