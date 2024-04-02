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

import undetected_chromedriver as uc
import time
import pandas as pd
from time import process_time
import json

with open('../../../Dictionary/Pro/MLB.json', 'r') as file:
    team_mappings = json.load(file)

def find_team_rank_name(dk_team_name):
    for team_mapping in team_mappings:
        if team_mapping["BetMGM Name"] == dk_team_name:
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

def find_element_text_or_not_found(driver, path, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, path))
        )
        return element.text
    except:
        return 'N/A'

def scrape(matchup_num):
   # matchup_num *= 2
    x = matchup_num - 1  # Indicates Away Team
    y = matchup_num      # Indicates Home Team
    away_team_text = find_element_text_or_not_found(driver, f'ms-six-pack-event.grid-event:nth-child({matchup_num}) > div:nth-child(2) > a:nth-child(1) > ms-event-detail:nth-child(1) > ms-event-name:nth-child(1) > ms-inline-tooltip:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)')
    home_team_text = find_element_text_or_not_found(driver, f'ms-six-pack-event.grid-event:nth-child{matchup_num}) > div:nth-child(2) > a:nth-child(1) > ms-event-detail:nth-child(1) > ms-event-name:nth-child(1) > ms-inline-tooltip:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1)')
    # away_spread_text = find_element_text_or_not_found(driver, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[1]/div/div/div/div[1]/span')
    # away_spread_odds_text = find_element_text_or_not_found(driver, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[1]/div/div/div/div[2]/div[2]/span')
    # total_text = find_element_text_or_not_found(driver, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[2]/div/div/div/div[1]/span[3]')
    # over_total_odds_text = find_element_text_or_not_found(driver, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[2]/div/div/div/div[2]/div[2]/span')
    # away_ml_text = find_element_text_or_not_found(driver, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[3]/div/div/div/div/div[2]/span')
    # home_spread_text = find_element_text_or_not_found(driver, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[1]/div/div/div/div[1]/span')
    # home_spread_odds_text = find_element_text_or_not_found(driver, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[1]/div/div/div/div[2]/div[2]/span')
    # under_total_odds_text = find_element_text_or_not_found(driver, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[2]/div/div/div/div[2]/div[2]/span')
    # home_ml_text = find_element_text_or_not_found(driver, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[3]/div/div/div/div/div[2]/span')
    # start_time_text = find_element_text_or_not_found(driver, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/th/a/div/div[1]/span')
    # away_team_rank_name = find_team_rank_name(away_team_text) #Name from team rankings.com
    # home_team_rank_name = find_team_rank_name(home_team_text) #Name from team rankings.com

    matchup = {
        'Away Team': away_team_text, 
        # 'Away Team Rank Name': away_team_rank_name, 
        # 'DK Away Odds': {
        #     'Spread': away_spread_text, 
        #     'Spread Odds': away_spread_odds_text, 
        #     'Away ML': away_ml_text
     #   }, 
        'Home Team': home_team_text, 
        # 'Home Team Rank Name': home_team_rank_name, 
        # 'DK Home Odds': {
        #     'Spread': home_spread_text, 
        #     'Spread Odds': home_spread_odds_text, 
        #     'Home ML': home_ml_text
        # },
        # 'Game': {
        #     'Start Time': start_time_text, 
        #     'Total': total_text, 
        #     'Over Total Odds': over_total_odds_text, 
        #     'Under Total Odds': under_total_odds_text,
        #     'League': 'NBA'
        # }
    }

    print(f'{away_team_text}, {home_team_text}')
    return matchup

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
service = Service(ChromeDriverManager().install())

# Initialize WebDriver without the 'desired_capabilities' argument
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://sports.nc.betmgm.com/en/sports/baseball-23/betting/usa-9/mlb-75")

time.sleep(10)  # Reduced sleep time after initial load
#specific_tbody = driver.find_element(By.CSS_SELECTOR, 'tbody.sportsbook-table__body')

data_file_path = '../games_count.json'
lock_file_path = '../games_count.lock'
lock = fasteners.InterProcessLock(lock_file_path)
number_of_games = read_games_count('MLB')


#num_rows = len(specific_tbody.find_elements(By.TAG_NAME, 'tr'))
#number_of_games = num_rows/2
all_matchups = []
#for z in range(1, int(number_of_games)+1):
#    print(f'{z}/{int(number_of_games)}')
#    matchup = scrape(z)
#    if matchup:
#        all_matchups.append(matchup)
for x in range(1, int(number_of_games)+1):
    matchup = scrape(x)  
    if matchup:
        all_matchups.append(matchup)
    else:
        break
#Writes to JSON
try:
   with open('../../Data/BetMGM/MLB.json', 'w') as fp:
       json.dump(all_matchups, fp, indent=4)
except Exception as e:
   print(f"Error writing to file: {e}")

driver.quit()

