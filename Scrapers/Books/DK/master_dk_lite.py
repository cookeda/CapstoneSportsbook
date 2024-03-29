import json

# Function to extract and reformat the relevant data from the original JSON file
def extract_relevant_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Define a new dictionary to hold the reformatted games with MatchupID as the key
    reformatted_games = {}
    for game_section in data:
            for game in game_section:
                # Extract the relevant data
                matchup_info = game['Info Table']
                odds_info = game['Odds Table']

                # Use the MatchupID as the key for the reformatted data
                matchup_id = game['MatchupID']
                reformatted_games[matchup_id] = {
                    'Home Team': matchup_info['Home Team Rank Name'],
                    'Away Team': matchup_info['Away Team Rank Name'],
                    'Home Spread': odds_info['Home Spread'],
                    'Away Spread': odds_info['Away Spread'],
                    'Total Points': odds_info['Total']
                }

        # Return the dictionary of reformatted games
    return reformatted_games

# Define the path to the original JSON file
original_file_path = '../../Data/DK/NBA.json'

# Extract and reformat the data
reformatted_data = extract_relevant_data(original_file_path)

# Save the reformatted data to a new JSON file
new_file_path = '../../Data/DK/NBA_Lite.json'
with open(new_file_path, 'w') as new_file:
    json.dump(reformatted_data, new_file, indent=4)

# Provide the path to the new JSON file
print(f"Reformatted JSON saved to: {new_file_path}")
