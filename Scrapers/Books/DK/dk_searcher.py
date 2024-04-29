import json
import sys

def load_data(filepath):
    """
    Load the JSON data from the file and convert it into a dictionary for O(1) lookup.
    The dictionary will map each BetTableId to its corresponding data.
    """
    with open(filepath, 'r', encoding = 'utf-8') as file:
        data = json.load(file)
        bet_table_dict = {}
        for item_list in data:
            for item in item_list:
                bet_table_id = item['BetTableId']
                bet_table_dict[bet_table_id] = item
    return bet_table_dict

def search_bet_table(bet_table_dict, bet_table_id):
    """
    Search for the given BetTableId in the dictionary.
    If found, returns only the 'Odds Table' data associated with the BetTableId,
    otherwise returns None.
    """
    result = bet_table_dict.get(bet_table_id, None)
    if result:
        return result.get('Odds Table', None)  # Return only the Odds Table
    return None

def main():
    # Check if the BetTableId was provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python matchup_searcher.py <BetTableId>")
        sys.exit(1)  # Exit the script indicating an error

    # The second argument on the command line should be the BetTableId
    search_id = sys.argv[1]

    # Replace the filepath with the actual path where the MLB.json is located
    filepath = '../../Data/DK/MLB.json'
    bet_table_dict = load_data(filepath)

    # Use the BetTableId from the command line to perform the search
    result = search_bet_table(bet_table_dict, search_id)
    if result is not None:
        print("Data Found: ", result)
    else:
        print("No data found for BetTableId:", search_id)
        
# Entry point for script execution
if __name__ == '__main__':
    main()