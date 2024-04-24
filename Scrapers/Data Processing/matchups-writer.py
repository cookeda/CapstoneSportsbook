import json
import sys

def extract_relevant_data(file_path):
    """
    Extracts and reformats data from a JSON file containing game information.

    This function reads a JSON file specified by the file_path parameter, extracts
    information about various games, and reformats this information into a more
    accessible structure. Each game's data is keyed by its MatchupID, and includes
    details such as team names, spreads, odds, and total points.

    Parameters:
    - file_path (str): The path to the JSON file containing the original game data.

    Returns:
    - dict: A dictionary where each key is a MatchupID and each value is another
      dictionary containing reformatted game information, including team names,
      spreads, odds, and total points.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    reformatted_games = {}
    for game in data:
        matchup_info = game['Info Table']
        odds_info = game['Odds Table']
        matchup_id = game['MatchupID']
        reformatted_games[matchup_id] = {
            'Home Team': matchup_info['Home Team Rank Name'],
            'Home Abv': matchup_info['Home Abv'],
            'Away Team': matchup_info['Away Team Rank Name'],
            'Away Abv': matchup_info['Away Abv'],
            'Home Spread': odds_info['Home Spread'].split(" ")[0],
            "Home Spread Book": odds_info['Home Spread'].split(" ")[1],
            'Home Spread Odds': odds_info['Home Spread Odds'].split(" ")[0],
            "Home Spread Odds Book": odds_info['Home Spread Odds'].split(" ")[1],
            'Home ML': odds_info['Home ML'].split(" ")[0],
            "Home ML Book": odds_info['Home ML'].split(" ")[1],
            'Away Spread': odds_info['Away Spread'].split(" ")[0],
            "Away Spread Book": odds_info['Away Spread'].split(" ")[1],
            'Away Spread Odds': odds_info['Away Spread Odds'].split(" ")[0],
            "Away Spread Odds Book": odds_info['Away Spread Odds'].split(" ")[1],
            'Away ML': odds_info['Away ML'].split(" ")[0],
            "Away ML Book": odds_info['Away ML'].split(" ")[1],
            'Total Points': odds_info['Total'].split(" ")[0],
            "Total Points Book": odds_info['Total'].split(" ")[1],
            'Over Odds': odds_info['Over Total Odds'].split(" ")[0],
            "Over Odds Book": odds_info['Over Total Odds'].split(" ")[1],
            'Under Odds': odds_info['Under Total Odds'].split(" ")[0],
            "Under Odds Book": odds_info['Under Total Odds'].split(" ")[1],
            'Time': matchup_info['Start Time'],
            'League': matchup_info["League"]
        }
    return reformatted_games

def main(input_file, output_file):
    """
    Main function to reformat data from an input JSON file and save it to an output file.

    This function takes the path to an input JSON file containing game information,
    reformats the data using the `extract_relevant_data` function, and then saves the
    reformatted data to an output JSON file. The output file is saved with UTF-8 encoding
    and the data is pretty-printed with an indentation of 4 spaces.

    Parameters:
    - input_file (str): The path to the input JSON file containing the original game data.
    - output_file (str): The path where the reformatted JSON data will be saved.

    Returns:
    - None: This function does not return any value. It outputs a file with the reformatted data.
    """
    reformatted_data = extract_relevant_data(input_file)
    with open(output_file, 'w', encoding='utf-8') as new_file:
        json.dump(reformatted_data, new_file, indent=4, ensure_ascii=False)
    print(f"Reformatted JSON saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python master_dk_lite.py <input_file_path> <output_file_path>")
    else:
        input_path = sys.argv[1]
        output_path = sys.argv[2]
        main(input_path, output_path)
