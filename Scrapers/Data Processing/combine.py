import json

def load_json(filename):
    """Utility function to load JSON data from a file."""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def merge_and_save_data(mlb_file, nba_file, output_file):
    """
    Load Best Book data and combines it.
    """
    # Load MLB and NBA data from files
    mlb_data = load_json(mlb_file)
    nba_data = load_json(nba_file)

    # Merge the data
    combined_data = mlb_data + nba_data

    # Save the merged data to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(combined_data, file, ensure_ascii=False, indent=4)

# Usage
merge_and_save_data('Clean/NBA/Best.json', 'Clean/MLB/Best.json', 'Clean/Best Odds.json')
#merge_and_save_data('Clean/NBA/Aggregate.json', 'Clean/MLB/Aggregate.json', '../../DegenBets/Data/Cleaned/AggregateOdds.json')
