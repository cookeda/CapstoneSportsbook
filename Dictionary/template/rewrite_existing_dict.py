import hashlib
import json
import zlib
import base64

# Function to hash the Team Rankings Name
def encode_team_data(team_name, league):
    # Combine team name, league, and current timestamp for uniqueness
    combined_str = f"{team_name}"
    
    # Convert to bytes and then encode to base64
    encoded_bytes = base64.b64encode(combined_str.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8')
    
    return encoded_str

def reformat_data(input_filename, output_filename):
    # Step 1: Load the data from the input JSON file
    with open(input_filename, 'r') as file:
        data = json.load(file)

    # Reformatted data
    reformatted_data = []
    for item in data:
        new_item = {
            "Team Rankings Name": item["Team Rankings Name"],
            "DraftKings Name": item["DraftKings Name"],
            "ESPNBet": item["ESPNBet"],  
            "BetMGM": item["BetMGM"],  
            "TeamID": encode_team_data(item["Team Rankings Name"], 'NBA'),
        }
        reformatted_data.append(new_item)

    # Step 2: Save the reformatted data back to the output JSON file
    with open(output_filename, 'w') as file:
        json.dump(reformatted_data, file, indent=4)

# Replace 'input.json' with the path to your actual input file and
# 'output.json' with your desired output file name.
reformat_data('../test/CBB.json', '../CBB.json')
