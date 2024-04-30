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
 
def process_ratings(rating, type, league):
    # Define a dictionary to handle the cases with scaled weights and star ratings
    cases = {
        'cover': {
            'NBA': lambda x: 3 if 5.5 <= x <= 6 else (2 if 6 <= x < 9 else (1 if 3 <= x < 6 else 0)),
            'MLB': lambda x: 3 if 12 <= x <= 15 else (2 if 0 <= x < 3 else (1 if 6 <= x < 9 else 0)),
        },
        'total': {
            'NBA': lambda x: -3 if 5.5 <= x <= 6 else (-2 if 5 <= x < 5.5 else (-1 if 4.5 <= x < 5 else (3 if 7 <= x else (2 if 6.5 <= x < 7 else (1 if  6.0 <= x < 6.5 else 0))))),
            'MLB': lambda x: -3 if 4.5 <= x <= 5.0 else (-2 if 5.5 <= x < 6 else (-1 if 5.0 <= x < 5.5 else (3 if 7 <= x else (2 if 6.5 <= x < 7 else (1 if  6.0 <= x < 6.5 else 0)))))
        }
    }

    '''MLB Scaling:

    Cover (MLB):
        3 stars: 0 to 3 range (34-34 record, balanced)
        2 stars: 3 to 6 range (19-25 record)
        1 star: 6 to 9 range (20-22 record)

    Total (Over MLB):
        3 stars: 6.5 to 7.0 range (2-1 record, limited instances but good performance)
        2 stars: 6 to 6.5 range (5-7 record)
        1 star: 7.0 to 7.5 range (0-1 record)

    Total (Under MLB):
        -3 stars: 5.0 to 5.5 range (37-18 record, strong performance)
        -2 stars: 4.5 to 5.0 range (20-15 record)
        -1 star: 4.0 to 4.5 range (5-8 record)

NBA Scaling:

    Cover (NBA):
        3 stars: 0 to 3 range (14-6 record, good performance)
        2 stars: 3 to 6 range (8-4 record)
        1 star: 6 to 9 range (3-1 record)

    Total (Under NBA):
        -3 stars: 5.5 to 6 range (9-4 record)
        -2 stars: 5.0 to 5.5 range (9-10 record, more balanced)
        -1 star: 4.5 to 5.0 range (2-2 record)'''

    # Get the sub-dictionary based on the type or return "Unknown" if type is not defined
    case = cases.get(type)

    if case:
        # Get the function based on the league or return "Unknown" if league is not defined
        func = case.get(league)
        if func:
            return func(rating)
        else:
            return "Unknown"
    else:
        return "Unknown"


def main():
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
                league = matchup_id[-3:]
                #print(league)

                cover_grade = process_ratings(cover_rating, 'cover', league)

                total_rating = process_ratings(over_score, 'total', league)

                # Store the data in the dictionary under the matchup ID, with details in a nested dictionary
                corrected[matchup_id] = {
                    "team_to_cover": team_to_cover,
                    "cover_rating": cover_rating,
                    "over_score": over_score,

                    "cover_grade": cover_grade,
                    "total_rating": total_rating,
                }
                i += 2  # Skip the next line as it's already processed
            else:
                i += 1

    # Write the processed results to a JSON file
    json_file_path = '../DegenBets/Data/master/game_summary.json'
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(corrected, json_file, indent=4)

    print(f"Data written to {json_file_path}")

if __name__ == '__main__':
    main()