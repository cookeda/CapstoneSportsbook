import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
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

def generate_game_id(away_team, home_team):
    combined_string = away_team + home_team
    hash_object = hashlib.md5(combined_string.encode())
    return hash_object.hexdigest()

def scrape(matchup_num):
    matchup_num *= 2
    x = matchup_num - 1  # Adjusted comment for clarity, indicates Away Team
    y = matchup_num      # Indicates Home Team
    try:
        # Adjust the WebDriverWait times based on observed average load times for efficiency
        away_team_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,  f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/th/a/div/div[2]/div/div/div/div'))
        )
        home_team_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,  f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/th/a/div/div[2]/div/div/div/div'))
        )
        away_spread_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,  f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[1]/div/div/div/div[1]/span'))
        )
        away_spread_odds_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,  f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[1]/div/div/div/div[2]/div[2]/span'))
        )
        total_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,  f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[2]/div/div/div/div[1]/span[3]'))
        )
        over_total_odds_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,  f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[2]/div/div/div/div[2]/div[2]/span'))
        )
        away_ml_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,  f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[3]/div/div/div/div/div[2]/span'))
        )
        home_spread_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,  f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[1]/div/div/div/div[1]/span'))
        )
        home_spread_odds_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,  f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[1]/div/div/div/div[2]/div[2]/span'))
        )
        under_total_odds_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,  f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[2]/div/div/div/div[2]/div[2]/span'))
        )
        home_ml_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,  f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[3]/div/div/div/div/div[2]/span'))
        )
        start_time_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,  f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/th/a/div/div[1]/span'))
        )
      
        matchup = {'Away Team' : away_team_element.text, 'DK Away Odds': {'Spread': away_spread_element.text, 'Spread Odds': away_spread_odds_element.text, 'Away ML': away_ml_element.text}, 
                   'Home Team' : home_team_element.text, 'DK Home Odds': {'Spread': home_spread_element.text, 'Spread Odds': home_spread_odds_element.text, 'Home ML': home_ml_element.text},
                   'Game': {'Start Time': start_time_element.text, 'Total': total_element.text, 'Over Total Odds': over_total_odds_element.text, 'Under Total Odds': under_total_odds_element.text},# 'GameID' : generate_game_id(away, home)}
        }

        #matchup = {'Away Team': away_team_element.text, 'Home Team': home_team_element.text}
        return matchup

    except Exception as e:
        print(f"Failed to scrape matchup {matchup_num//2}")#: {e}")
        return None  # Return None if there's an issue, allowing the loop to continue

driver = webdriver.Edge()
driver.get("https://sportsbook.draftkings.com/leagues/basketball/ncaab")


# Adjust the initial sleep time based on the minimum required time for initial page load
# Consider using WebDriverWait for a specific element that indicates the page has fully loaded to reduce unnecessary waiting
time.sleep(10)  # Reduced sleep time after initial load
specific_tbody = driver.find_element(By.CSS_SELECTOR, 'tbody.sportsbook-table__body')

num_rows = len(specific_tbody.find_elements(By.TAG_NAME, 'tr'))
number_of_games = num_rows/2
#print(number_of_games)
#number_of_games = len(rows)  # Keep the dynamic determination of games if possible, else hard-coded for simplicity here
all_matchups = []

for z in range(1, int(number_of_games)+1):
    print(f'{z}/{int(number_of_games)+1}')
    matchup = scrape(z)
    if matchup:
        all_matchups.append(matchup)

try:
    with open('Scrapers/Data/cbbdk.json', 'w') as fp:
        json.dump(all_matchups, fp, indent=4)
except Exception as e:
    print(f"Error writing to file: {e}")

driver.quit()

