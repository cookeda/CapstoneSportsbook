import json  # Import the json module
import zlib

# Read the contents of the uploaded file
file_path = 'game_results.txt'

def extract_team_to_cover(line):
    """Safely extract the team recommended to cover the spread from a given line."""
    # Search for the pattern in the line
    if "Bet on" in line and "to cover the spread." in line:
        # Extract the team name by splitting the line
        parts = line.split("Bet on ")[1].split(" to cover the spread.")
        team_to_bet_on = parts[0]
        return team_to_bet_on
    else:
        return "No betting recommendation found in the line."


def get_hash(value):
    return format(zlib.crc32(value.encode()), 'x')

def encode_matchup_id(away_id, home_id, league):
    if away_id and home_id:
        return f'{away_id}_{home_id}_{league}'
    return "Unknown"

def get_matchup_id_for_game(game_info):
    # Split the game info to extract team names and league
    parts = game_info.split(" @ ")
    away_team = parts[0]
    home_team_and_league = parts[1].split(" (")
    home_team = home_team_and_league[0]
    league = home_team_and_league[1].rstrip(")")

    # Generate team IDs
    away_id = get_hash(away_team)
    home_id = get_hash(home_team)

    # Generate and return the matchup ID
    return encode_matchup_id(away_id, home_id, league)
 
corrected = {}
# Re-opening the file to re-process with the corrected logic
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if "Cover Rating" in line and "Over Score" in line:
            game_info = line.split(":")[0].strip()

            if i+1 < len(lines):
                team_to_cover = extract_team_to_cover(lines[i+1].strip())
            else:
                team_to_cover = "No betting recommendation found."
            
            cover_rating = float(line.split("Cover Rating - ")[1].split(",")[0])
            over_score = float(line.split("Over Score - ")[1].split("\n")[0])
            
            matchup_id = get_matchup_id_for_game(game_info)

            # Store the data in the dictionary under the matchup ID, with details in a nested dictionary
            corrected[matchup_id] = {
                "team_to_cover": team_to_cover,
                "cover_rating": cover_rating,
                "over_score": over_score
            }
            i += 2  # Skip the next line as it's already processed
        else:
            i += 1

# Write the processed results to a JSON file
json_file_path = '../DegenBets/Data/master/game_summary.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(corrected, json_file, indent=4)

print(f"Data written to {json_file_path}")