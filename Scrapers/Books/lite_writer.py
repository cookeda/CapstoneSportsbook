import json
import sys

def extract_relevant_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    reformatted_games = {}
    for game_section in data:
        for game in game_section:
            matchup_info = game['Info Table']
            odds_info = game['Odds Table']
            matchup_id = game['MatchupID']
            reformatted_games[matchup_id] = {
                'Home Team': matchup_info['Home Team Rank Name'],
                'Away Team': matchup_info['Away Team Rank Name'],
                'Home Spread': odds_info['Home Spread'],
                'Home Spread Odds': odds_info['Home Spread Odds'],
                'Away Spread': odds_info['Away Spread'],
                'Away Spread Odds': odds_info['Away Spread Odds'],
                'Total Points': odds_info['Total'],
                'Over Odds': odds_info['Over Total Odds'],
                'Under Odds' : odds_info['Under Total Odds'],

            }
    return reformatted_games

def main(input_file, output_file):
    reformatted_data = extract_relevant_data(input_file)
    with open(output_file, 'w') as new_file:
        json.dump(reformatted_data, new_file, indent=4)
    print(f"Reformatted JSON saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python master_dk_lite.py <input_file_path> <output_file_path>")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        main(input_path, output_path)