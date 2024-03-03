import hashlib
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
        print(away_team_element.text)

        # Keep the structure for later use, if needed
        # Home team element retrieval could be added here with a similar structure

        matchup = {'Away Team': away_team_element.text}
        return matchup

    except Exception as e:
        print(f"Failed to scrape matchup {matchup_num//2}: {e}")
        return None  # Return None if there's an issue, allowing the loop to continue

driver = uc.Chrome()
driver.get("https://sportsbook.draftkings.com/leagues/basketball/ncaab")

# Adjust the initial sleep time based on the minimum required time for initial page load
# Consider using WebDriverWait for a specific element that indicates the page has fully loaded to reduce unnecessary waiting
time.sleep(10)  # Reduced sleep time after initial load

number_of_games = 10  # Keep the dynamic determination of games if possible, else hard-coded for simplicity here
all_matchups = []

for z in range(1, number_of_games + 1):
    matchup = scrape(z)
    if matchup:
        all_matchups.append(matchup)

try:
    with open('cbbdk.json', 'w') as fp:
        json.dump(all_matchups, fp, indent=4)
except Exception as e:
    print(f"Error writing to file: {e}")

driver.quit()

  # home_team_element = WebDriverWait(driver, 10).until(
   #     EC.visibility_of_element_located((By.XPATH,  f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/th/a/div/div[2]/div/div/div/div/div'))
   # )    #away_team = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/th/a/div/div[2]/div/div/div/div').text
    #home_team = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/th/a/div/div[2]/div/div/div/div/div').text
    #away_spread = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[1]/div/div/div/div[1]/span').text 
    #away_spread_odds = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[1]/div/div/div/div[2]/div[2]/span').text
    #total = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[2]/div/div/div/div[1]/span[3]').text
    #over_total_odds = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[2]/div/div/div/div[2]/div[2]/span').text
    #away_ml = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/td[3]/div/div/div/div/div[2]/span').text
    #home_spread = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[1]/div/div/div/div[1]/span').text 
    #home_spread_odds= driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[1]/div/div/div/div[2]/div[2]/span').text
    #under_total_odds = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[2]/div/div/div/div[2]/div[2]/span').text
    #home_ml = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(y)}]/td[3]/div/div/div/div/div[2]/span').text
    #start_time = driver.find_element(By.XPATH, f'/html/body/div[2]/div[2]/section/section[2]/section/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[{str(x)}]/th/a/div/div[1]/span').text