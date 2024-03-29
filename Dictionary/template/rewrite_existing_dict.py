import hashlib
import json
import zlib

# Function to hash the Team Rankings Name
def get_hash(value):
    return format(zlib.crc32(value.encode()), 'x')

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
            "TeamID": (item["TeamID"])
        }
        reformatted_data.append(new_item)

    # Step 2: Save the reformatted data back to the output JSON file
    with open(output_filename, 'w') as file:
        json.dump(reformatted_data, file, indent=4)

# Replace 'input.json' with the path to your actual input file and
# 'output.json' with your desired output file name.
reformat_data('Pro/NFL.json', 'NFL.json')
