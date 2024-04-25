import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import fasteners
import os
import logging



import time
import pandas as pd
from time import process_time
import json
# For Connor
webdriver.chrome
logging.getLogger('scrapy').setLevel(logging.INFO)

live_games = 0 

league = 'NBA'
book = 'DK'

with open('../../../Dictionary/Pro/NBA.json', 'r', encoding='utf-8') as file:
    team_mappings = json.load(file)

def encode_bet_table_id(matchup_id, book_name):
    """
    Generates a unique identifier for a betting table based on the matchup ID and the book name.

    Parameters:
    - matchup_id (str): The unique identifier for the matchup.
    - book_name (str): The name of the bookmaker.

    Returns:
    - str: A unique identifier for the bet table in the format '{book_name}_{matchup_id}'.
          If either `matchup_id` or `book_name` is missing, it returns "Unknown".
    """
    if matchup_id and book_name:
        return f'{book_name}_{matchup_id}'
    return "Unknown" 

def encode_matchup_id(away_id, home_id, league):
    """
    Generates a unique identifier for a matchup based on the IDs of the away and home teams, and the league.

    Parameters:
    - away_id (str): The unique identifier for the away team.
    - home_id (str): The unique identifier for the home team.
    - league (str): The name of the league in which the matchup occurs.

    Returns:
    - str: A unique identifier for the matchup in the format '{away_id}_{home_id}_{league}'.
          If either `away_id` or `home_id` is missing, it returns "Unknown".
    """
    if away_id and home_id:
        return f'{away_id}_{home_id}_{league}'
    return "Unknown"

def find_team_id(team_name):
    """
    Searches for a team's ID based on its name from a predefined mapping.

    This function iterates through a global list of team mappings, each being a dictionary
    that contains the team's name as it appears on DraftKings and its corresponding unique TeamID.
    If a match is found, the TeamID is returned. If no match is found, a default value of "Unknown" is returned.

    Parameters:
    - team_name (str): The name of the team as it appears on DraftKings.

    Returns:
    - str: The unique TeamID associated with the given team name. Returns "Unknown" if no match is found.
    """
    for team_mapping in team_mappings:
        if team_mapping["DraftKings Name"] == team_name:
            return team_mapping["TeamID"]
    return "Unknown"  # Return a default value if not found


def find_abv(team_name):
    """
    Searches for a team's ID based on its name from a predefined list of team mappings.

    Parameters:
    - team_name (str): The name of the team as recognized by DraftKings.

    Returns:
    - str: The unique TeamID associated with the given team name. Returns "Unknown" if the team name is not found in the mappings.
    """
    for team_mapping in team_mappings:
        if team_mapping["DraftKings Name"] == team_name:
            return team_mapping["PlainText"]
    return "Unknown"  # Return a default value if not found

def find_team_rank_name(dk_team_name):
    """
    Searches for a team's ranking name based on its DraftKings name from a predefined mapping.

    This function iterates through a global list of team mappings, each being a dictionary
    that contains the team's name as it appears on DraftKings and its corresponding ranking name
    as it appears on TeamRankings.com. If a match is found, the Team Rankings Name is returned.
    If no match is found, a default value of "Unknown" is returned.

    Parameters:
    - dk_team_name (str): The name of the team as it appears on DraftKings.

    Returns:
    - str: The ranking name of the team as it appears on TeamRankings.com. Returns "Unknown" if no match is found.
    """
    for team_mapping in team_mappings:
        if team_mapping["DraftKings Name"] == dk_team_name:
            return team_mapping["Team Rankings Name"]
    return "Unknown"  # Return a default value if not found  # Return a default value if not found


match = {}

def clean_team(raw_team):
    """
    Cleans and formats the team name extracted from the raw text.

    This function takes a raw team name string, splits it by space, and selects the second part
    (assuming the first part is a common prefix or identifier not needed). It then converts this
    part to uppercase. If the team name is 'TRAIL', it corrects it to 'TRAILBLAZERS' to handle
    a specific case of abbreviation.

    Parameters:
    - raw_team (str): The raw team name string to be cleaned.

    Returns:
    - str: The cleaned and formatted team name.
    """
    team = raw_team.split(" ")
    team = team[1].upper()
    if team == 'TRAIL':
        team = 'TRAILBLAZERS'
    return team

def generate_game_id(away_team, home_team):
    """
    Generates a unique game identifier using MD5 hashing.

    This function takes the names of the away and home teams, concatenates them,
    and then applies MD5 hashing to the combined string to generate a unique identifier
    for a game. This identifier can be used to uniquely identify a game in a dataset or database.

    Parameters:
    - away_team (str): The name of the away team.
    - home_team (str): The name of the home team.

    Returns:
    - str: A unique identifier for the game, generated using MD5 hashing.
    """
    combined_string = away_team + home_team
    hash_object = hashlib.md5(combined_string.encode())
    return hash_object.hexdigest()

def find_element_text_or_not_found(driver, xpath, wait_time=10):
    """
    Attempts to find an element on a web page using its CSS selector and returns its text. 
    If the element is not found within the specified wait time, returns a default value.

    Parameters:
    - driver: The Selenium WebDriver instance used to interact with the web page.
    - xpath (str): The CSS selector of the element to find.
    - wait_time (int, optional): The maximum number of seconds to wait for the element to become visible. Defaults to 10 seconds.

    Returns:
    - str: The text of the found element. If the element is not found within the wait time, returns '-999'.
    """
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, xpath))
        )
        return element.text
    except:
        return '-999'

def update_games_count(game_type, number_of_games):
    """
    Updates the count of games for a specific game type in a JSON file.

    This function first checks if the JSON file exists and has content. If it does, it loads the existing data.
    If the file does not exist or is empty, it initializes an empty dictionary. It then updates the game count
    for the specified game type and writes the updated data back to the JSON file.

    Parameters:
    - game_type (str): The type of game (e.g., 'NBA') for which the count is being updated.
    - number_of_games (int): The number of games to be recorded for the specified game type.

    Returns:
    - None
    """
    with lock:
        # Check if the file exists and has content
        if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
            with open(data_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = {}
        
        # Update the data
        data[game_type] = number_of_games
        
        # Write the updated data back to the file
        with open(data_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

def update_live_games_count(game_type, number_of_games):
    """
    Updates the count of games for a specific game type in a JSON file.

    This function first checks if the JSON file exists and has content. If it does, it loads the existing data into a dictionary. If the file does not exist or is empty, it initializes an empty dictionary. It then updates the game count for the specified game type and writes the updated dictionary back to the JSON file.

    Parameters:
    - game_type (str): The type of game (e.g., 'MLB') for which the count is being updated.
    - number_of_games (int): The new count of games to be recorded for the specified game type.

    No return value.
    """
    with lock:
        # Check if the file exists and has content
        if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
            with open(data_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        else:
            data = {}
        
        # Update the data
        data[game_type] = number_of_games
        
        # Write the updated data back to the file
        with open(data_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

def read_games_count(game_type):
    """
    Reads the count of games for a specific game type from a JSON file.

    This function checks if the JSON file exists and has content. If so, it opens the file,
    loads the data, and attempts to retrieve the count of games for the specified game type.
    If the file does not exist, is empty, or the game type is not found, the function returns None.

    Parameters:
    - game_type (str): The type of game (e.g., 'NBA') for which the count is being queried.

    Returns:
    - int or None: The count of games for the specified game type if found, otherwise None.
    """
    with lock:
        if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
            with open(data_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get(game_type)
        return None  # Or appropriate error handling/alternative return value


def scrape(matchup_num):
    """
    Scrapes betting information for a specific matchup from DraftKings' sportsbook page.

    This function uses Selenium to navigate the DOM of the DraftKings sportsbook page and extract
    information about a specific matchup. It constructs a detailed dictionary containing the matchup ID,
    betting odds, team information, and other relevant details.

    Parameters:
    - matchup_num (int): The matchup number on the sportsbook page. This is used to calculate the
      specific DOM elements to target for scraping.

    Returns:
    - list: A list containing a single dictionary with detailed information about the matchup,
      including betting odds and team information.
    """
    matchup_num *= 2
    x = matchup_num - 1  # Indicates Away Team
    y = matchup_num      # Indicates Home Team

    # Extracting text information for both teams and various betting odds using specific CSS selectors
    away_team_text = find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > th:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')
    home_team_text = find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({y}) > th:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')
    away_spread_text = find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')
    away_spread_odds_text = find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')
    total_text = find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > td:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(3)')
    over_total_odds_text = find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > td:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')
    away_ml_text = find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > td:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)')
    home_spread_text = find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({y}) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')
    home_spread_odds_text = find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({y}) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')
    under_total_odds_text = find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({y}) > td:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')
    home_ml_text = find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({y}) > td:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)')
    start_time_text = find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > th:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)')
    
    # Finding team rank names and IDs using predefined functions
    away_team_rank_name = find_team_rank_name(away_team_text)  # Name from team rankings.com
    home_team_rank_name = find_team_rank_name(home_team_text)  # Name from team rankings.com
    away_team_id = find_team_id(away_team_text)  # Team ID for away team
    home_team_id = find_team_id(home_team_text)  # Team ID for home team
    
    # Generating unique identifiers for the matchup and bet table
    matchup_id = encode_matchup_id(away_team_id, home_team_id, league)
    bet_table_id = encode_bet_table_id(matchup_id, book)
    
    # Compiling all extracted information into a structured dictionary
    away_abv = find_abv(away_team_text)
    home_abv = find_abv(home_team_text)

    if start_time_text == '-999': 
        live_games =+ 1
        print(x)

        
    info = [ 
        {
            'BetTableId': bet_table_id,
            'Odds Table': {
                'Book Name': book, 
                'Away Spread': away_spread_text, 
                'Away Spread Odds': away_spread_odds_text,
                'Away ML': (away_ml_text),
                'Home Spread': home_spread_text, 
                'Home Spread Odds': home_spread_odds_text,
                'Home ML': (home_ml_text),
                'Total': total_text, 
                'Over Total Odds': (over_total_odds_text), 
                'Under Total Odds': (under_total_odds_text),
            },
            'MatchupID': matchup_id,
            'Info Table': {                
                    'Away Team': away_team_text, 
                    'Away Team Rank Name': away_team_rank_name,
                    'Away Abv': away_abv,
                    'Away ID': away_team_id,
                    'Home Team': home_team_text, 
                    'Home Team Rank Name': home_team_rank_name,
                    'Home Abv': home_abv,
                    'Home ID': home_team_id, 
                    'Start Time': start_time_text, 
                    'League': league
                }
            }
        
    ]
    print(f'{away_team_text}, {home_team_text}')
    return info
#For Devin
#driver = webdriver.Firefox()

#For Connor
options = Options()
options.add_argument('--headless')
options.add_argument('log-level=3')

# Initialize the Service
service = Service(ChromeDriverManager().install())

# Initialize WebDriver without the 'desired_capabilities' argument
driver = webdriver.Chrome(service=service, options=options)


driver.get("https://sportsbook.draftkings.com/leagues/basketball/nba")


time.sleep(10)  # Reduced sleep time after initial load
specific_tbody = driver.find_element(By.CSS_SELECTOR, '.parlay-card-10-a')

num_rows = len(specific_tbody.find_elements(By.TAG_NAME, 'tr'))
number_of_games = num_rows/2
all_matchups = []
for z in range(1, int(number_of_games)+1):
    print(f'{league} - {book}: {z}/{int(number_of_games)}')
    matchup = scrape(z)
    if matchup:
        all_matchups.append(matchup)

driver.quit()

data_file_path = '../games_count.json'
lock_file_path = '../games_count.lock'

lock = fasteners.InterProcessLock(lock_file_path)

update_games_count('NBA', int(live_games))

data_file_path = '../live_games_count.json'
lock_file_path = '../live_games_count.lock'


lock = fasteners.InterProcessLock(lock_file_path)

update_live_games_count('NBA', (live_games))
print(live_games)

        
#Writes to JSON
try:
    with open('../../Data/DK/NBA.json', 'w', encoding='utf-8') as fp:
        json.dump(all_matchups, fp, indent=4, ensure_ascii=False)
except Exception as e:
    print(f"Error writing to file: {e}")


