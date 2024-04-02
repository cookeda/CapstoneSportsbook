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

league = 'NBA'
book = 'DK'

with open('../../../Dictionary/Pro/NBA.json', 'r') as file:
    team_mappings = json.load(file)

def encode_bet_table_id(matchup_id, book_name):
    if matchup_id and book_name:
        return f'{book_name}_{matchup_id}'
    return "Unknown" 

def encode_matchup_id(away_id, home_id, league):
    if away_id and home_id:
        return f'{away_id}_{home_id}_{league}'
    return "Unkown"

def find_team_id(team_name):
    for team_mapping in team_mappings:
        if team_mapping["DraftKings Name"] == team_name:
            return team_mapping["TeamID"]
    return "Unknown"  # Return a default value if not found


def find_team_rank_name(dk_team_name):
    for team_mapping in team_mappings:
        if team_mapping["DraftKings Name"] == dk_team_name:
            return team_mapping["Team Rankings Name"]
    return "Unknown"  # Return a default value if not found


match = {}

def clean_team(raw_team):
    team = raw_team.split(" ")
    team = team[1].upper()
    if team == 'TRAIL':
        team = 'TRAILBLAZERS'
    return team

def generate_game_id(away_team, home_team):
    combined_string = away_team + home_team
    hash_object = hashlib.md5(combined_string.encode())
    return hash_object.hexdigest()

def find_element_text_or_not_found(driver, xpath, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, xpath))
        )
        return element.text
    except:
        return 'N/A'

def update_games_count(game_type, number_of_games):
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
    with lock:
        if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
            with open(data_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get(game_type)
        return None  # Or appropriate error handling/alternative return value


def scrape(matchup_num):
    matchup_num *= 2
    x = matchup_num - 1  # Indicates Away Team
    y = matchup_num      # Indicates Home Team

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
                'Total': total_text[2:], 
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


driver.get("https://sportsbook.draftkings.com/leagues/basketball/nba")


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

update_games_count('NBA', int(number_of_games))
        
#Writes to JSON
try:
    with open('../../Data/DK/NBA.json', 'w', encoding='utf-8') as fp:
        json.dump(all_matchups, fp, indent=4, ensure_ascii=False)
except Exception as e:
    print(f"Error writing to file: {e}")


