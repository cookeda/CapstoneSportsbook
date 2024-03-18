import json

#input file path
file_path = 'Dictionary/temp/nfl_names.json'
with open(file_path, 'r') as fp:
    data = json.load(fp)
# Dictionary to hold all the data
list = []

# Populate the dictionary with team names and blank stats
for team in data:
    list.append({
        "Team Rankings Name": team,
        "DraftKings Name": "",
        "FanDuel Name": "",
        "BetMGM Name": "",
        "Pinnacle Name": "",
        "TeamID": ""
    })

output_file = 'Dictionary/Pro/nfl_teams.json'
# Save the dictionary to a JSON file
with open(output_file, 'w') as f:
    json.dump(list, f, indent=4)

print("Skeleton JSON file created successfully.")