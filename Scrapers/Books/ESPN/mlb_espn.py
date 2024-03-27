import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import undetected_chromedriver as uc
import time
import pandas as pd
from time import process_time
import json

with open('../../../Dictionary/College/NCAAB Teams.json', 'r') as file:
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
    matchup_num *= 2
    x = matchup_num - 1  # Indicates Away Team
    y = matchup_num      # Indicates Home Team

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
    #away_team_rank_name = find_team_rank_name(away_team_text) #Name from team rankings.com
    #home_team_rank_name = find_team_rank_name(home_team_text) #Name from team rankings.com
    # List of all the odds text variables
    

    matchup = {
        'Away Team': away_team_text, 
    #    'Away Team Rank Name': away_team_rank_name, 
        'ESPN Away Odds': {
            'Spread': away_spread_text, 
            'Spread Odds': check_even(away_spread_odds_text), 
            'Away ML': check_even(away_ml_text)
        }, 
        'Home Team': home_team_text, 
    #    'Home Team Rank Name': home_team_rank_name, 
        'ESPN Home Odds': {
            'Spread': home_spread_text, 
            'Spread Odds': check_even(home_spread_odds_text), 
            'Home ML': check_even(home_ml_text)
        },
        'Game': {
            'Start Time': start_time_text, 
            'Total': total_text, 
            'Over Total Odds': check_even(over_total_odds_text), 
            'Under Total Odds': check_even(under_total_odds_text),
            'League' : 'NBA'
        }
    }

    print(f'{away_team_text}, {home_team_text}')
    return matchup

options = Options()
options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
driver.get("https://espnbet.com/sport/baseball/organization/united-states/competition/mlb/featured-page")


time.sleep(10)  # Reduced sleep time after initial load
#specific_tbody = driver.find_element(By.CSS_SELECTOR, 'tbody.sportsbook-table__body')

#num_rows = len(specific_tbody.find_elements(By.TAG_NAME, 'tr'))
number_of_games = 1# num_rows/2
all_matchups = []
z = 1  # Start with the first matchup

while True:
    print(f'Scraping matchup number: {z}')
    try:
        matchup = scrape(z)
        if matchup:
            all_matchups.append(matchup)
            z += 1  # Increment only if a matchup was found
        else:
            # If scrape returns None or empty, it indicates no more matchups
            break
    except Exception as e:
        # If an exception is thrown, assume no more matchups can be found
        print(f"An error occurred: {e}")
        break

print(f'Total matchups scraped: {len(all_matchups)}')

#all_matchups.append(scrape(1))

#print(len(driver.find_elements_by_class_name('b-divider')))
#Writes to JSON
try:
    with open('../../Data/ESPN/MLB.json', 'w') as fp:
        json.dump(all_matchups, fp, indent=4)
except Exception as e:
    print(f"Error writing to file: {e}")

driver.quit()
