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

import time
import pandas as pd
from time import process_time
import json
# For Connor
webdriver.chrome

league = 'CBB'
book = 'DK'

with open('../../../Dictionary/College/CBB.json', 'r', encoding='utf-8') as file:
    team_mappings = json.load(file)

def encode_bet_table_id(matchup_id, book_name):
    """
    Generates a unique identifier for a betting table based on the matchup ID and the book name.

    Parameters:
    - matchup_id (str): The unique identifier for the matchup.
    - book_name (str): The name of the bookmaker.

    Returns:
    - str: A string that combines the book name and the matchup ID, separated by an underscore.
          If either the matchup_id or book_name is missing, it returns "Unknown".
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
    - league (str): The league in which the matchup is taking place.

    Returns:
    - str: A string that combines the away team ID, home team ID, and league, separated by underscores.
          If either the away_id or home_id is missing, it returns "Unknown".
    """
    if away_id and home_id:
        return f'{away_id}_{home_id}_{league}'
    return "Unkown"

def find_team_id(team_name):
    """
    Searches for a team's ID based on its name from a predefined list of team mappings.

    Parameters:
    - team_name (str): The name of the team as recognized by DraftKings.

    Returns:
    - str: The unique TeamID associated with the given team name. If the team name is not found,
           returns "Unknown".
    """
    for team_mapping in team_mappings:
        if team_mapping["DraftKings Name"] == team_name:
            return team_mapping["TeamID"]
    return "Unknown"  # Return a default value if not found

def find_team_rank_name(dk_team_name):
    """
    Searches for and returns the team's name as recognized by Team Rankings based on the DraftKings name.

    This function iterates through a predefined list of team mappings, each mapping containing the team's name
    as recognized by DraftKings and its corresponding name as recognized by Team Rankings. The function matches
    the provided DraftKings name with its counterpart in the list and returns the Team Rankings name.

    Parameters:
    - dk_team_name (str): The name of the team as recognized by DraftKings.

    Returns:
    - str: The name of the team as recognized by Team Rankings. If the DraftKings name is not found in the
           predefined list, it returns "Unknown".
    """
    for team_mapping in team_mappings:
        if team_mapping["DraftKings Name"] == dk_team_name:
            return team_mapping["Team Rankings Name"]
    return "Unknown"  # Return a default value if not found  # Return a default value if not found


match = {}

def clean_team(raw_team):
    """
    Cleans and formats the team name extracted from raw data.

    This function takes a raw team name string, splits it by space, and selects the second part (assuming the first part is a prefix or identifier not needed). It then converts this part to uppercase. If the resulting team name is 'TRAIL', it corrects it to 'TRAILBLAZERS' to handle a specific case of abbreviation.

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

    This function takes the names of the away and home teams, concatenates them, and then applies MD5 hashing to the combined string to generate a unique identifier for a game. This identifier can be used to uniquely identify a game in a dataset or database.

    Parameters:
    - away_team (str): The name of the away team.
    - home_team (str): The name of the home team.

    Returns:
    - str: A hexadecimal string representing the MD5 hash of the concatenated team names, serving as a unique game identifier.
    """
    combined_string = away_team + home_team
    hash_object = hashlib.md5(combined_string.encode())
    return hash_object.hexdigest()

def find_element_text_or_not_found(driver, xpath, wait_time=10):
    """
    Attempts to find an element on a web page based on its CSS selector and returns its text. If the element is not found within the specified wait time, it returns 'N/A'.

    Parameters:
    - driver: The Selenium WebDriver instance used to interact with the web page.
    - xpath (str): The CSS selector of the element to find.
    - wait_time (int, optional): The maximum time in seconds to wait for the element to become visible. Defaults to 10 seconds.

    Returns:
    - str: The text of the found element, or '-999' if the element is not found or not visible within the wait time.
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

    This function checks if the JSON file exists and has content. If it does, it loads the existing data,
    updates the count for the specified game type, and then writes the updated data back to the file.
    If the file does not exist or is empty, it creates a new dictionary, adds the game type and count,
    and writes this data to the file.

    Parameters:
    - game_type (str): The type of game (e.g., 'CBB' for College Basketball) to update the count for.
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
        
        # Update the data with the new games count for the specified game type
        data[game_type] = number_of_games
        
        # Write the updated data back to the file
        with open(data_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

def read_games_count(game_type):
    """
    Reads the count of games for a specific game type from a JSON file.

    This function checks if the JSON file exists and has content. If it does, it opens the file,
    loads the data, and retrieves the count for the specified game type. If the file does not exist,
    is empty, or the game type is not found, it returns None.

    Parameters:
    - game_type (str): The type of game (e.g., 'CBB' for College Basketball) for which the count is requested.

    Returns:
    - int or None: The count of games for the specified game type if found, otherwise None.
    """
    with lock:
        if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
            with open(data_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get(game_type)
        return None

def scrape(matchup_num):
    """
    Scrapes betting information for a specific matchup from a web page using Selenium.

    This function navigates through the web page to find and extract betting information for a given matchup.
    It uses the matchup number to locate the correct elements on the page and extracts details such as team names,
    spread, moneyline (ML), total points, and odds. It also generates unique identifiers for the matchup and the
    betting table using helper functions.

    Parameters:
    - matchup_num (int): The number of the matchup to scrape. This is used to calculate the positions of elements
                         on the page related to the away and home teams.

    Returns:
    - list: A list containing a dictionary with the scraped betting information, including a unique bet table ID,
            odds table, matchup ID, and information table with team details and start time.
    """
    matchup_num *= 2
    x = matchup_num - 1  # Indicates Away Team
    y = matchup_num      # Indicates Home Team

    # Extracting text information for both teams, their spreads, moneylines, total points, and odds using XPath.
    away_team_text = find_element_text_or_not_found(driver, f'div.parlay-card-10-a:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({x}) > th:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)')
    home_team_text = find_element_text_or_not_found(driver, f'div.parlay-card-10-a:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({y}) > th:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)')
    away_spread_text = find_element_text_or_not_found(driver, f'div.parlay-card-10-a:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({x}) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')
    away_spread_odds_text = find_element_text_or_not_found(driver, f'div.parlay-card-10-a:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({x}) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')
    total_text = find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > td:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)')
    
    over_total_odds_text = find_element_text_or_not_found(driver, f'div.parlay-card-10-a:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({x}) > td:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')
    away_ml_text = find_element_text_or_not_found(driver, f'div.parlay-card-10-a:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({x}) > td:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)')
    home_spread_text = find_element_text_or_not_found(driver, f'div.parlay-card-10-a:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({y}) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')
    home_spread_odds_text = find_element_text_or_not_found(driver, f'div.parlay-card-10-a:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({y}) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')
    under_total_odds_text = find_element_text_or_not_found(driver, f'div.parlay-card-10-a:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({y}) > td:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')
    home_ml_text = find_element_text_or_not_found(driver, f'div.parlay-card-10-a:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({y}) > td:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)')
    start_time_text = find_element_text_or_not_found(driver, f'div.parlay-card-10-a:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({x}) > th:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)')
    away_team_rank_name = find_team_rank_name(away_team_text) #Name from team rankings.com
    home_team_rank_name = find_team_rank_name(home_team_text) #Name from team rankings.com
    away_team_id = find_team_id(away_team_text) #Team
    home_team_id = find_team_id(home_team_text) #Team
    matchup_id = encode_matchup_id(away_team_id, home_team_id, league)
    bet_table_id = encode_bet_table_id(matchup_id, book)
    
    info = [ 
        {
            'BetTableId': bet_table_id,
            'Odds Table': {
                'Book Name': 'DK',
                'Away Spread': away_spread_text, 
                'Away Spread Odds': away_spread_odds_text,
                'Away ML': (away_ml_text),
                'Home Spread': home_spread_text, 
                'Home Spread Odds': home_spread_odds_text,
                'Home ML': (home_ml_text),
                'Total': total_text[3:], 
                'Over Total Odds': (over_total_odds_text), 
                'Under Total Odds': (under_total_odds_text),
            },
            'MatchupID': matchup_id,
            'Info Table': {                
                    'Away Team': away_team_text, 
                    'Away Team Rank Name': away_team_rank_name, 
                    'Away ID': away_team_id,
                    'Home Team': home_team_text, 
                    'Home Team Rank Name': home_team_rank_name,
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


driver.get("https://sportsbook.draftkings.com/leagues/basketball/ncaab")


time.sleep(10)  # Reduced sleep time after initial load
specific_tbody = driver.find_element(By.CSS_SELECTOR, '.parlay-card-10-a')

num_rows = len(specific_tbody.find_elements(By.TAG_NAME, 'tr'))
number_of_games = num_rows/2
all_matchups = []
for z in range(1, int(number_of_games)+1):
    print(f'{z}/{int(number_of_games)}')
    matchup = scrape(z)
    if matchup:
        all_matchups.append(matchup)
driver.quit()


data_file_path = '../games_count.json'
lock_file_path = '../games_count.lock'

lock = fasteners.InterProcessLock(lock_file_path)

update_games_count('CBB', int(number_of_games))

#Writes to JSON
try:
    with open('../../Data/DK/CBB.json', 'w', encoding='utf-8') as fp:
        json.dump(all_matchups, fp, indent=4, ensure_ascii=False)
except Exception as e:
    print(f"Error writing to file: {e}")


