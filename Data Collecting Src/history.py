import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date as dt, timedelta
from selenium.webdriver.chrome.options import Options
import json

def scrapeYesterday(yesterday):
    link = "https://plaintextsports.com/all/"

    options = Options()
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    driver = webdriver.Chrome(options=options)

    driver.get(link + yesterday)
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    driver.quit()
    return soup

def getMatchups(soup, yesterday):
    leagues = soup.find_all('div', class_='text-center font-bold')
    matchups_data = []
    matchup_tracker = {}  # To track matchups and identify double headers

    for league in leagues:
        league_name = league.get_text().strip()
        mapping_dict = None
        regex_pattern = None
        if league_name == "National Basketball Association":
            league_name = "NBA"
            mapping_dict = load_team_mappings("../Dictionary/Pro/NBA.json")
            regex_pattern = r"([A-Z]+)\s*(?:\d+W\s+)?(\d+)"
        elif league_name == "Major League Baseball":
            league_name = "MLB"
            mapping_dict = load_team_mappings("../Dictionary/Pro/MLB.json")
            regex_pattern = r"([A-Z]+)\s*(\d+)(?:/\d+)?(?:\s+[A-Z]+)?\s*$"
        elif league_name == "NCAA Men's Basketball":
            league_name = "CBB"
            mapping_dict = load_team_mappings("../Dictionary/College/CBB.json")
            regex_pattern = r"([A-Za-z ]+)\s+(\d+)"

        games = league.find_next_sibling('div', class_='flex flex-wrap justify-evenly')
        if games and league_name in ("NBA", "MLB", "CBB"):
            matchups = games.find_all('div')
            for matchup in matchups:
                teams_scores_text = matchup.get_text(strip=True).split('|')[1:-1]
                teams_scores = [ts.strip() for ts in teams_scores_text if ts.strip()]

                if len(teams_scores) >= 3:
                    try:
                        away_team_score_match = re.search(regex_pattern, teams_scores[1])
                        home_team_score_match = re.search(regex_pattern, teams_scores[2])

                        if away_team_score_match and home_team_score_match:
                            away_team, away_score = away_team_score_match.groups()
                            home_team, home_score = home_team_score_match.groups()

                            away_team = away_team.strip()
                            home_team = home_team.strip()

                            matchup_id = f"{away_team} vs {home_team}"
                            is_double_header = matchup_id in matchup_tracker
                            matchup_tracker[matchup_id] = True

                            matchup_info = {
                                'Date': yesterday,
                                'League': league_name,
                                'Away Team': get_city_name_from_abbreviation(away_team, mapping_dict),
                                'Away Score': away_score,
                                'Home Team': get_city_name_from_abbreviation(home_team, mapping_dict),
                                'Home Score': home_score,
                                'IsDoubleHeader': is_double_header
                            }
                            matchups_data.append(matchup_info)
                        else:
                            print(f"Problematic matchup data: {teams_scores}")
                    except AttributeError as e:
                        print(f"Skipping a matchup due to an error: {e}")
                        print(f"Problematic matchup data: {teams_scores}")

    matchups_df = pd.DataFrame(matchups_data)
    if not matchups_df.empty:
        return matchups_df
    else:
        print("No data was extracted.")
    return None

def save_to_csv(df, filename):
    # Save DataFrame to a CSV, appending if it exists.
    try:
        df.to_csv(filename, mode='w', header=False, index=False)
    except FileNotFoundError:
        df.to_csv(filename, mode='w', header=True, index=False)

def load_from_csv(file_path, column_names):
    return pd.read_csv(file_path, header=None, names=column_names)

def append_to_csv(file_path, data):
    # Append data to a CSV file, creating the file if it does not exist
    data.to_csv(file_path, mode='a', header=not pd.io.common.file_exists(file_path), index=False)


def load_team_mappings(directory):
    with open(directory, 'r') as file:
        teams = json.load(file)
    # Create a dictionary that maps the abbreviation to the full city name
    abbreviation_to_city = {}
    for team in teams:
        plaintext = team["PlainText"]
        abbreviation_to_city[plaintext] = team["Team Rankings Name"]
    return abbreviation_to_city

def get_city_name_from_abbreviation(abbreviation, mapping_dict):
    return mapping_dict.get(abbreviation, abbreviation)  # Return "Unknown" if not found

def movePreditionsToDailyPredictions():
    f = open("../OddsHistory/History/IfYouSeeThisItWorked.txt", "x")
    f.write(dt.today())
    f.close()
    predictions_columns = ['date', 'league', 'cover_rating', 'betting_advice', 'over_score', 'home_spread',
                           'away_spread', 'total', 'away_team', 'home_team']
    predictions = load_from_csv("../OddsHistory/History/Predictions.csv", predictions_columns)
    save_to_csv(predictions, "../OddsHistory/History/DailyPredictions.csv")



# Takes all history and outputs data.
# Will add most recent game matchups to history.
def compare_and_update():
    # Define column names based on CSV structure
    predictions_columns = ['date', 'league', 'cover_rating', 'betting_advice', 'over_score', 'home_spread',
                           'away_spread', 'total', 'away_team', 'home_team']
    history_columns = ['date', 'league', 'away_team', 'away_team_score', 'home_team', 'home_team_score',
                       'second_game_doubleheader']

    # Load the data
    predictions = load_from_csv("../OddsHistory/History/DailyPredictions.csv", predictions_columns)
    history = load_from_csv("../OddsHistory/History/MatchupHistory.csv", history_columns)

    # Ensure that the 'date' and 'league' columns are of the same data type (string)
    predictions['date'] = predictions['date'].astype(str)
    predictions['league'] = predictions['league'].astype(str)
    history['date'] = history['date'].astype(str)
    history['league'] = history['league'].astype(str)

    #print("Unique Teams in Predictions:", sorted(predictions['away_team'].unique()),
    #      sorted(predictions['home_team'].unique()))
    #print("Unique Teams in History:", sorted(history['away_team'].unique()), sorted(history['home_team'].unique()))

    # Merge and compare data
    comparison = pd.merge(predictions, history, on=['date', 'league', 'away_team', 'home_team'], how='left')
    comparison['cover_correct'] = False
    comparison['total_correct'] = False

    for index, row in comparison.iterrows():
        actual_spread = row['home_team_score'] - row['away_team_score']
        if row['betting_advice'] == row['home_team']:
            predicted_spread = row['home_spread']
            cover_correct = actual_spread > -predicted_spread
        else:
            predicted_spread = row['away_spread']
            cover_correct = actual_spread < predicted_spread
        comparison.at[index, 'cover_correct'] = cover_correct

        total_points = row['home_team_score'] + row['away_team_score']

        # Split for Totals
        comparison_value = 6
        comparison.at[index, 'total_correct'] = (row['over_score'] > comparison_value and total_points > row[
            'total']) or \
                                                (row['over_score'] <= comparison_value and total_points < row['total'])

    # Append results to the cumulative CSV
    append_to_csv('../OddsHistory/History/CumulativeResults.csv',
                  comparison[['date', 'league', 'betting_advice', 'cover_correct', 'cover_rating', 'total_correct', 'over_score']])


def main():
    yesterday = (dt.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    comparison_columns = ['date', 'league', 'betting_advice', 'cover_correct', 'cover_rating', 'total_correct', 'over_score']
    comparison_csv = load_from_csv("../OddsHistory/History/CumulativeResults.csv", comparison_columns)

    # Check if yesterday's data already exists
    if not comparison_csv['date'].str.contains(yesterday).any():
        df = getMatchups(scrapeYesterday(yesterday), yesterday)
        save_to_csv(df, "../OddsHistory/History/MatchupHistory.csv")
        compare_and_update()
    else:
        print("ALREADY RAN TODAY. DID NOT RUN")

if __name__ == "__main__":
    main()
