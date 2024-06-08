import json
import zlib
import pandas as pd
import numpy as np
import re

file_path = 'game_results.txt'

def extract_team_to_cover(line):
    if "Bet on" in line and "to cover the spread." in line:
        parts = line.split("Bet on ")[1].split(" to cover the spread.")
        return parts[0]
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
    league_match = re.search(r'\((.*?)\)', game_info)
    if league_match:
        league = league_match.group(1)
    else:
        league = "Unknown"

    # Generate team IDs
    away_id = get_hash(away_team)
    home_id = get_hash(home_team)

    # Generate and return the matchup ID
    return encode_matchup_id(away_id, home_id, league)
 
def dynamic_process_ratings(df, column, league):
    # This function replaces the previous static mapping with a dynamic one
    # Define thresholds for star ratings dynamically based on percentiles
    # thresholds = np.percentile(df[column], [33, 66, 100])  # Calculate thresholds as 33rd, 66th, and 100th percentiles
    # labels = [1, 2, 3] if column == 'cover_rating' else [-1, -2, -3]
    # df['grade'] = pd.cut(df[column], bins=[-np.inf] + list(thresholds), labels=labels, right=False)
    # return df['grade']

    df[column] = pd.to_numeric(df[column], errors='coerce')
    df = df.dropna(subset=[column])  # Drop rows with NaN values in the column

    # Check if the column is empty after cleaning
    if df[column].empty:
        print(f"No valid data in column '{column}' for league '{league}'.")
        return pd.Series([0]*len(df), index=df.index)

    # Calculate thresholds as 33rd, 66th, and 100th percentiles
    thresholds = np.percentile(df[column], [33, 66, 100])
    labels = [1, 2, 3] if column == 'cover_rating' else [-1, -2, -3]
    df['grade'] = pd.cut(df[column], bins=[-np.inf] + list(thresholds), labels=labels, right=False)
    return df['grade']

def main():
    corrected = {}
    df = pd.DataFrame(columns=['matchup_id', 'league', 'cover_rating', 'over_score', 'team_to_cover'])

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 2):
            game_info = lines[i].strip()
            if "Cover Rating" in game_info and "Over Score" in game_info:
                if i+1 < len(lines):
                    team_to_cover = extract_team_to_cover(lines[i+1].strip())
                else:
                    team_to_cover = "No betting recommendation found."
                cover_rating = float(game_info.split("Cover Rating - ")[1].split(",")[0])
                over_score = float(game_info.split("Over Score - ")[1])

                matchup_id = get_matchup_id_for_game(game_info)
                league = matchup_id.split('_')[-1]

                corrected[matchup_id] = {
                    "team_to_cover": team_to_cover,
                    "cover_rating": cover_rating,
                    "over_score": over_score
                }

                df = df._append({'matchup_id': matchup_id, 'league': league, 'cover_rating': cover_rating, 'over_score': over_score, 'team_to_cover': team_to_cover}, ignore_index=True)

    # Process ratings dynamically
    df['cover_grade'] = dynamic_process_ratings(df, 'cover_rating', df['league'])
    df['total_rating'] = dynamic_process_ratings(df, 'over_score', df['league'])


    # Update the corrected dictionary with dynamic ratings
    for index, row in df.iterrows():
        cover_grade = row['cover_grade']
        total_rating = row['total_rating']
            
        # Replace NaN or empty values with 0
        if pd.isna(cover_grade) or cover_grade == "":
            cover_grade = 0
        if pd.isna(total_rating) or total_rating == "":
            total_rating = 0
        
        corrected[row['matchup_id']].update({
            'cover_grade': cover_grade,
            'total_rating': total_rating
        })


    # Write the processed results to a JSON file
    json_file_path = '../DegenBets/Data/master/game_summary.json'
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(corrected, json_file, indent=4, ensure_ascii=False)

    print(f"Data written to {json_file_path}")

if __name__ == '__main__':
    main()
