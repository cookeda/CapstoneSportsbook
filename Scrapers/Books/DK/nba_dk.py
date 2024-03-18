import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from time import process_time
import json
# For Connor
webdriver.chrome

with open('Dictionary/Pro/NBA.json', 'r') as file:
    team_mappings = json.load(file)

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

    matchup = {
        'Away Team': away_team_text, 
        'Away Team Rank Name': away_team_rank_name, 
        'DK Away Odds': {
            'Spread': away_spread_text, 
            'Spread Odds': away_spread_odds_text, 
            'Away ML': away_ml_text
        }, 
        'Home Team': home_team_text, 
        'Home Team Rank Name': home_team_rank_name, 
        'DK Home Odds': {
            'Spread': home_spread_text, 
            'Spread Odds': home_spread_odds_text, 
            'Home ML': home_ml_text
        },
        'Game': {
            'Start Time': start_time_text, 
            'Total': total_text, 
            'Over Total Odds': over_total_odds_text, 
            'Under Total Odds': under_total_odds_text,
            'League': 'NBA'
        }
    }

    print(f'{away_team_text}, {home_team_text}')
    return matchup

#For Devin
#driver = webdriver.Firefox()

#For Connor
driver = webdriver.Chrome()
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
        
#Writes to JSON
try:
    with open('Scrapers/Data/DK/NBA.json', 'w', encoding='utf-8') as fp:
        json.dump(all_matchups, fp, indent=4, ensure_ascii=False)
except Exception as e:
    print(f"Error writing to file: {e}")

driver.quit()

