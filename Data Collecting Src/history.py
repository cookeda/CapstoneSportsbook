import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date as dt, timedelta
from selenium.webdriver.chrome.options import Options

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
        if league_name == "National Basketball Association":
            league_name = "NBA"
        elif league_name == "Major League Baseball":
            league_name = "MLB"
        elif league_name == "NCAA Men's Basketball":
            league_name = "CBB"

        games = league.find_next_sibling('div', class_='flex flex-wrap justify-evenly')
        if games and league_name in ("NBA", "MLB", "CBB"):
            matchups = games.find_all('div')
            for matchup in matchups:
                teams_scores_text = matchup.get_text(strip=True).split('|')[1:-1]
                teams_scores = [ts.strip() for ts in teams_scores_text if ts.strip()]

                if len(teams_scores) >= 3:  # Checks for the 'Final' marker and two teams
                    try:
                        away_team_score_match = re.search(r"(.+?)\s+(\d+)$", teams_scores[1])
                        home_team_score_match = re.search(r"(.+?)\s+(\d+)$", teams_scores[2])

                        if away_team_score_match and home_team_score_match:
                            away_team, away_score = away_team_score_match.groups()
                            home_team, home_score = home_team_score_match.groups()

                            # Formulate a unique identifier for each matchup based on the teams
                            matchup_id = f"{away_team} vs {home_team}"

                            is_double_header = False
                            if matchup_id in matchup_tracker:
                                # If this matchup has occurred before today, mark this as the second game
                                is_double_header = True
                            else:
                                matchup_tracker[matchup_id] = True  # Mark this matchup as seen

                            matchup_info = {
                                'Date': yesterday,
                                'League': league_name,
                                'Away Team': away_team,
                                'Away Score': away_score,
                                'Home Team': home_team,
                                'Home Score': home_score,
                                'IsDoubleHeader': is_double_header  #to indicate second game of a double header
                            }
                            matchups_data.append(matchup_info)
                        else:
                            print(f"Problematic matchup data: {teams_scores}")
                    except AttributeError as e:
                        print(f"Skipping a matchup due to an error: {e}")
                        print(f"Problematic matchup data: {teams_scores}")

    matchups_df = pd.DataFrame(matchups_data)
    if not matchups_df.empty:
        print(matchups_df)
    else:
        print("No data was extracted.")
    return matchups_df

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

# Takes all history and outputs data.
# Will add most recent game matchups to history.
def compare_and_update():
    # Define column names based on CSV structure
    predictions_columns = ['date', 'league', 'cover_rating', 'betting_advice', 'over_score', 'home_spread',
                           'away_spread', 'total']
    history_columns = ['date', 'league', 'away_team', 'away_team_score', 'home_team', 'home_team_score',
                       'second_game_doubleheader']

    # Load the data
    predictions = load_from_csv("../OddsHistory/History/Predictions.csv", predictions_columns)
    history = load_from_csv("../OddsHistory/History/MatchupHistory.csv", history_columns)

    # Ensure that the 'date' and 'league' columns are of the same data type (string)
    predictions['date'] = predictions['date'].astype(str)
    predictions['league'] = predictions['league'].astype(str)
    history['date'] = history['date'].astype(str)
    history['league'] = history['league'].astype(str)

    # Merge and compare data
    comparison = pd.merge(predictions, history, on=['date', 'league'], how='inner')
    comparison['cover_correct'] = False
    comparison['total_correct'] = False

    for index, row in comparison.iterrows():
        predicted_spread = row['home_spread'] if row['betting_advice'] == row['home_team'] else row['away_spread']
        actual_spread = row['home_team_score'] - row['away_team_score']
        comparison.at[index, 'cover_correct'] = (actual_spread > predicted_spread and row['betting_advice'] == row[
            'home_team']) or (actual_spread < predicted_spread and row['betting_advice'] == row['away_team'])

        total_points = row['home_team_score'] + row['away_team_score']
        comparison.at[index, 'total_correct'] = (row['over_score'] > 5 and total_points > row['total']) or (
                    row['over_score'] < 5 and total_points < row['total'])

    # Append results to the cumulative CSV
    append_to_csv('../OddsHistory/History/CumulativeResults.csv',
                  comparison[['date', 'league', 'betting_advice', 'cover_correct', 'total_correct']])


def main():
    #yesterday = (dt.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    # TESTING PURPOSES COMMENT OUT CODE BELOW
    yesterday = dt.today().strftime('%Y-%m-%d')
    df = getMatchups(scrapeYesterday(yesterday), yesterday)
    save_to_csv(df, "../OddsHistory/History/MatchupHistory.csv")
    compare_and_update()

if __name__ == "__main__":
    main()

