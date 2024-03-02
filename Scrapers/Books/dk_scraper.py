import hashlib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC, wait

import undetected_chromedriver as uc
import time
import pandas as pd
from time import process_time
import json

match = {}

def clean_team(raw_team):
    team = raw_team.split(" ")
    team = team[1].upper()
    if team == 'TRAIL':
        team = 'TRAILBLAZERS'
    return team

#Hashes game id using a concat of team names, cleaned for the format of CELTICS, NETS, (Team name only all caps)
def generate_game_id(away_team, home_team):
    combined_string = away_team + home_team
    hash_object = hashlib.md5(combined_string.encode())
    return hash_object.hexdigest()

def scrape(matchup_num):
    matchup_num *= 2
    x = matchup_num - 1 #Indicates Aqay Team
    y = matchup_num #Indicates Home Team

    away_team = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/th/a/div/div[2]/div/div/div/div/div').text
    home_team = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/th/a/div/div[2]/div/div/div/div/div').text
    away_spread = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[1]/div/div/div/div[1]/span').text 
    away_spread_odds = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[1]/div/div/div/div[2]/div[2]/span').text
    total = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[2]/div/div/div/div[1]/span[3]').text
    over_total_odds = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[2]/div/div/div/div[2]/div[2]/span').text
    away_ml = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[3]/div/div/div/div/div[2]/span').text
    home_spread = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[1]/div/div/div/div[1]/span').text 
    home_spread_odds= driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[1]/div/div/div/div[2]/div[2]/span').text
    under_total_odds = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[2]/div/div/div/div[2]/div[2]/span').text
    home_ml = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[3]/div/div/div/div/div[2]/span').text
    start_time = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/th/a/div/div[1]/span').text
    
    away = clean_team(away_team)
    home = clean_team(home_team)    

    matchup = {'Away Team' : away, 'DK Away Odds': {'Spread': away_spread, 'Spread Odds': away_spread_odds, 'Away ML': away_ml}, 
               'Home Team' : home, 'DK Home Odds': {'Spread': home_spread, 'Spread Odds': home_spread_odds, 'Home ML': home_ml},
               'Game': {'Start Time': start_time, 'Total': total, 'Over Total Odds': over_total_odds, 'Under Total Odds': under_total_odds, 'GameID' : generate_game_id(away, home)}
    }
    return matchup


driver = uc.Chrome()

driver.get("https://sportsbook.draftkings.com/leagues/basketball/nba")
#driver.get("https://sportsbook.draftkings.com/leagues/basketball/ncaab")
time.sleep(5)
#Still need a live number of games
number_of_games = 5
all_matchups = []

for z in range(1, number_of_games + 1):
    matchup = scrape(z)
    if matchup:
        all_matchups.append(matchup)
try:
    with open('dk.json', 'w') as fp:
        json.dump(all_matchups, fp, indent=4)
except Exception as e:
    print(f"Error writing to file: {e}")
driver.quit()
