import hashlib
import json
import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc


with open('../../../Dictionary/Pro/CBB.json', 'r') as file:
    team_mappings = json.load(file)

def encode_bet_table_id(matchup_id, book_name):
    """
    Generates a unique identifier for a betting table based on the matchup ID and the book name.

    Parameters:
    - matchup_id (str): The unique identifier for the matchup.
    - book_name (str): The name of the bookmaker.

    Returns:
    - str: A string that combines the book name and the matchup ID, separated by an underscore.
          Returns "Unknown" if either the matchup_id or book_name is missing.
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
    - league (str): The name of the league in which the matchup is taking place.

    Returns:
    - str: A string that combines the away team ID, home team ID, and league, separated by underscores.
          Returns "Unknown" if either the away_id or home_id is missing.
    """
    if away_id and home_id:
        return f'{away_id}_{home_id}_{league}'
    return "Unknown"

def find_team_id(team_name):
    """
    Searches for a team's ID based on its name.

    This function iterates through a predefined list of team mappings (team_mappings) to find a team's ID using its name. The search is based on the "ESPNBet" key in each mapping, which should match the provided team name.

    Parameters:
    - team_name (str): The name of the team for which the ID is being searched.

    Returns:
    - str: The ID of the team if found, otherwise returns "Unknown".
    """
    for team_mapping in team_mappings:
        if team_mapping["ESPNBet"] == team_name:
            return team_mapping["TeamID"]
    return "Unknown"  # Return a default value if not found

def find_team_rank_name(dk_team_name):
    """
    Searches for a team's ranking name based on its name used in DraftKings (DK).

    This function iterates through a predefined list of team mappings (team_mappings) to find a team's ranking name using its DraftKings name. The search is based on the "ESPNBet" key in each mapping, which should match the provided team name from DraftKings. If a match is found, the function returns the team's ranking name as listed in "Team Rankings Name".

    Parameters:
    - dk_team_name (str): The name of the team as used in DraftKings.

    Returns:
    - str: The ranking name of the team if found, otherwise returns "Unknown".
    """
    for team_mapping in team_mappings:
        if team_mapping["ESPNBet"] == dk_team_name:
            return team_mapping["Team Rankings Name"]
    return "Unknown"  # Return a default value if not found  # Return a default value if not found


match = {}

def clean_team(raw_team: str) -> str:
    """
    Clean a team name from the raw team name.

    Parameters:
    raw_team (str): The raw team name.

    Returns:
    str: The cleaned team name.
    """
    team = raw_team.split(" ")
    team = team[1].upper()
    if team == 'TRAIL':
        team = 'TRAILBLAZERS'
    return team

def generate_game_id(away_team, home_team):
    """
    Generates a unique game identifier using MD5 hashing.

    This function takes the names of the away and home teams, concatenates them, and then applies MD5 hashing to generate a unique identifier for a game. This identifier can be used to distinguish games in databases or logs where unique identification of games is required.

    Parameters:
    - away_team (str): The name of the away team.
    - home_team (str): The name of the home team.

    Returns:
    - str: A hexadecimal string representing the MD5 hash of the concatenated team names.
    """
    combined_string = away_team + home_team
    hash_object = hashlib.md5(combined_string.encode())
    return hash_object.hexdigest()


def find_element_text_or_default(driver, xpath, default='N/A', wait_time=10):
    """Finds text of a web element by xpath, returns default if not found within wait time."""
    try:
        element = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return element
    except Exception:
        return default

def hash_teams(away_team, home_team):
    """Creates an MD5 hash for a game based on the team names."""
    hash_input = away_team + home_team
    return hashlib.md5(hash_input.encode()).hexdigest()

# Initialize the Chrome driver with undetected_chromedriver to avoid detection
options = uc.ChromeOptions()
options.headless = True
options.add_argument('--no-sandbox')
driver = uc.Chrome(options=options)

driver.get("https://sportsbook.caesars.com/us/wa-ms/bet?dl=retail_mode")
time.sleep(5)  # Allow some time for the page to load JavaScript content

# Replace 'your_xpath' with the actual XPaths for the elements
matchup_xpath = '//div[contains(@class,"Matchup")]'
print(find_element_text_or_default(driver, "/html/body/div[2]/div/div[11]/div/div[1]/div/div[2]/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div/div/a[1]/div/div/div[2]/div/span"))
