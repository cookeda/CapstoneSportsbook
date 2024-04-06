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

import requests
import undetected_chromedriver as uc
import time
import threading
import pandas as pd
from time import process_time
import json

league = 'NBA'
book = 'ESPN'

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
        if team_mapping["ESPNBet"] == team_name:
            return team_mapping["TeamID"]
    return "Unknown"  # Return a default value if not found

def find_team_rank_name(dk_team_name):
    for team_mapping in team_mappings:
        if team_mapping["ESPNBet"] == dk_team_name:
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
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        return element.text
    except:
        return 'N/A'

#Espn has +100 odds set to 'Even'
def check_even(text):
    if text == 'Even':
        return '+100'
    return text

def scrape(matchup_num):
    #matchup_num *= 2
    #x = matchup_num - 1  # Indicates Away Team
    #y = matchup_num      # Indicates Home Team

    away_team_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[2]/div[1]/button/div/div/div[1]')
    home_team_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[3]/div[1]/button/div/div/div[1]')
    away_spread_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[2]/div[2]/button[1]/span[1]')
    away_spread_odds_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[2]/div[2]/button[1]/span[2]')
    total_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[2]/div[2]/button[2]/span[1]')
    over_total_odds_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[2]/div[2]/button[2]/span[2]')
    away_ml_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[2]/div[2]/button[3]/span[2]')
    home_spread_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[3]/div[2]/button[1]/span[1]')
    home_spread_odds_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[3]/div[2]/button[1]/span[2]')
    under_total_odds_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[3]/div[2]/button[2]/span[2]')
    home_ml_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[3]/div[2]/button[3]/span[2]')
    start_time_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/div/div[2]/div[{matchup_num}]/div/div[1]/button/span')
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



def managed_webdriver(*args, **kwargs):
    driver = webdriver.Chrome(*args, **kwargs)
    try:
        yield driver
    finally:
        driver.quit()
def read_games_count(game_type):
    with lock:
        if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
            with open(data_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get(game_type)
        return None  # Or appropriate error handling/alternative return value


options = Options()
options.add_argument('--headless')
options.add_argument('log-level=3')

# Initialize the Service
service = Service(ChromeDriverManager().install())

# Initialize WebDriver without the 'desired_capabilities' argument
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://espnbet.com/sport/basketball/organization/united-states/competition/nba/featured-page")

time.sleep(10)  # Reduced sleep time after initial load
#specific_tbody = driver.find_element(By.CSS_SELECTOR, 'tbody.sportsbook-table__body')

#num_rows = len(specific_tbody.find_elements(By.TAG_NAME, 'tr'))
data_file_path = '../games_count.json'
lock_file_path = '../games_count.lock'
lock = fasteners.InterProcessLock(lock_file_path)


number_of_games = read_games_count('NBA')
all_matchups = []
for z in range(1, int(number_of_games)+1):
    print(f'{league} - {book}: {z}/{int(number_of_games)}')
    matchup = scrape(z)
    if matchup:
        all_matchups.append(matchup)

print(f'Total matchups scraped: {len(all_matchups)}')
driver.quit()


#Writes to JSON
try:
    with open('../../Data/ESPN/NBA.json', 'w', encoding='utf-8') as fp:
        json.dump(all_matchups, fp, indent=4)
except Exception as e:
    print(f"Error writing to file: {e}")


#TODO: Only Scrape todays matches
#TODO: Fix freeze bug
#TODO: Fix dictionary for ESPN
