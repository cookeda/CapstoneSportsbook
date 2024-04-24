import json

# Paths to the source JSON files
game_summary_path = '../DegenBets/Data/master/game_summary.json'
matchups_path = '../DegenBets/Data/script/matchups.json'

# Path to the output JSON file
merged_path = '../DegenBets/Data/merged_data.json'

def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def main():
    # Load the game summary and matchups data
    game_summary = load_data(game_summary_path)
    matchups = load_data(matchups_path)

    # Merge the data based on matchup ID
    merged_data = {}
    for matchup_id in matchups:
        if matchup_id in game_summary:
            merged_data[matchup_id] = {**matchups[matchup_id], **game_summary[matchup_id]}
        else:
            print(f"Warning: No game summary found for matchup ID {matchup_id}")

    # Save the merged data to a new file
    with open(merged_path, 'w', encoding='utf-8') as outfile:
        json.dump(merged_data, outfile, indent=4, ensure_ascii=False)

    print("Merging complete. Data saved to 'merged_data.json'.")

if __name__ == "__main__":
    main()