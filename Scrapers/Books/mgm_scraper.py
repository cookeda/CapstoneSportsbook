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

def clean_team(raw_team):
    team = raw_team.upper()
    return team

def generate_game_id(away_team, home_team):
    combined_string = away_team + home_team
    hash_object = hashlib.md5(combined_string.encode())
    return hash_object.hexdigest()

def scrape(matchup_num):
    matchup_num *= 2
    x = matchup_num - 1
    y = matchup_num
    away_team = driver.find_element(By.XPATH, f'/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar/div/div/div/div/ms-main-column/div/ms-widget-layout/ms-widget-slot[3]/ms-composable-widget[1]/ms-widget-slot/ms-tabbed-grid-widget/ms-grid/div/ms-event-group/ms-six-pack-event[1]/div[2]/a/ms-event-detail/ms-event-name/ms-inline-tooltip/div/div[{str(x)}]/div/div/div[1]/div').text
    home_team = driver.find_element(By.XPATH, f'/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar/div/div/div/div/ms-main-column/div/ms-widget-layout/ms-widget-slot[3]/ms-composable-widget[1]/ms-widget-slot/ms-tabbed-grid-widget/ms-grid/div/ms-event-group/ms-six-pack-event[1]/div[2]/a/ms-event-detail/ms-event-name/ms-inline-tooltip/div/div[{str(y)}]/div/div/div[1]/div').text
    away_spread = driver.find_element(By.XPATH, f'/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar/div/div/div/div/ms-main-column/div/ms-widget-layout/ms-widget-slot[3]/ms-composable-widget[1]/ms-widget-slot/ms-tabbed-grid-widget/ms-grid/div/ms-event-group/ms-six-pack-event[1]/div[2]/div/div/ms-option-group[1]/ms-option[{str(x)}]/ms-event-pick/div/div[1]/div').text 
    away_spread_odds = driver.find_element(By.XPATH, f'/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar/div/div/div/div/ms-main-column/div/ms-widget-layout/ms-widget-slot[3]/ms-composable-widget[1]/ms-widget-slot/ms-tabbed-grid-widget/ms-grid/div/ms-event-group/ms-six-pack-event[1]/div[2]/div/div/ms-option-group[1]/ms-option[{str(x)}]/ms-event-pick/div/div[2]/ms-font-resizer').text
    total = driver.find_element(By.XPATH, f'/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar/div/div/div/div/ms-main-column/div/ms-widget-layout/ms-widget-slot[3]/ms-composable-widget[1]/ms-widget-slot/ms-tabbed-grid-widget/ms-grid/div/ms-event-group/ms-six-pack-event[1]/div[2]/div/div/ms-option-group[2]/ms-option[{str(x)}]/ms-event-pick/div/div[1]/div').text
    over_total_odds = driver.find_element(By.XPATH, f'/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar/div/div/div/div/ms-main-column/div/ms-widget-layout/ms-widget-slot[3]/ms-composable-widget[1]/ms-widget-slot/ms-tabbed-grid-widget/ms-grid/div/ms-event-group/ms-six-pack-event[1]/div[2]/div/div/ms-option-group[2]/ms-option[{str(x)}]/ms-event-pick/div/div[2]/ms-font-resizer').text
    away_ml = driver.find_element(By.XPATH, f'/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar/div/div/div/div/ms-main-column/div/ms-widget-layout/ms-widget-slot[3]/ms-composable-widget[1]/ms-widget-slot/ms-tabbed-grid-widget/ms-grid/div/ms-event-group/ms-six-pack-event[1]/div[2]/div/div/ms-option-group[3]/ms-option[{str(x)}]/ms-event-pick/div/div[2]/ms-font-resizer').text
    home_spread = driver.find_element(By.XPATH, f'/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar/div/div/div/div/ms-main-column/div/ms-widget-layout/ms-widget-slot[3]/ms-composable-widget[1]/ms-widget-slot/ms-tabbed-grid-widget/ms-grid/div/ms-event-group/ms-six-pack-event[1]/div[2]/div/div/ms-option-group[1]/ms-option[{str(y)}]/ms-event-pick/div/div[1]/div').text 
    home_spread_odds= driver.find_element(By.XPATH, f'/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar/div/div/div/div/ms-main-column/div/ms-widget-layout/ms-widget-slot[3]/ms-composable-widget[1]/ms-widget-slot/ms-tabbed-grid-widget/ms-grid/div/ms-event-group/ms-six-pack-event[1]/div[2]/div/div/ms-option-group[1]/ms-option[{str(y)}]/ms-event-pick/div/div[2]/ms-font-resizer').text
    under_total_odds = driver.find_element(By.XPATH, f'/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar/div/div/div/div/ms-main-column/div/ms-widget-layout/ms-widget-slot[3]/ms-composable-widget[1]/ms-widget-slot/ms-tabbed-grid-widget/ms-grid/div/ms-event-group/ms-six-pack-event[1]/div[2]/div/div/ms-option-group[2]/ms-option[{str(y)}]/ms-event-pick/div/div[2]/ms-font-resizer').text
    home_ml = driver.find_element(By.XPATH, f'/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar/div/div/div/div/ms-main-column/div/ms-widget-layout/ms-widget-slot[3]/ms-composable-widget[1]/ms-widget-slot/ms-tabbed-grid-widget/ms-grid/div/ms-event-group/ms-six-pack-event[1]/div[2]/div/div/ms-option-group[3]/ms-option[{str(y)}]/ms-event-pick/div/div[2]/ms-font-resizer').text
    start_time = driver.find_element(By.XPATH, f'/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar/div/div/div/div/ms-main-column/div/ms-widget-layout/ms-widget-slot[3]/ms-composable-widget[1]/ms-widget-slot/ms-tabbed-grid-widget/ms-grid/div/ms-event-group/ms-six-pack-event[{str(x)}]/div[1]/div/ms-event-info/ms-event-timer/ms-prematch-timer').text
    

    start_time = start_time.split(" • ")[1]
    clean_total = total.split(" ")[1]

    away = clean_team(away_team)
    home = clean_team(home_team)    

    matchup = {'Away Team' : away, 'MGM Away Odds': {'Spread': away_spread, 'Spread Odds': away_spread_odds, 'Away ML': away_ml}, 
               'Home Team' : home, 'MGM Home Odds': {'Spread': home_spread, 'Spread Odds': home_spread_odds, 'Home ML': home_ml},
               'Game': {'Start Time': start_time, 'Total': clean_total, 'Over Total Odds': over_total_odds, 'Under Total Odds': under_total_odds, 'GameID' : generate_game_id(away, home)}
    }
    print(matchup)
    return matchup


driver = uc.Chrome()

driver.get("https://sports.az.betmgm.com/en/sports?wm=7006663&btag=&tdpeh=&pid=")
time.sleep(15)
#Still need a live number of games
number_of_games = 1
all_matchups = []
for z in range(1, number_of_games):
    all_matchups.append(scrape(z))
with open('mgm.json', 'w') as fp:
    json.dump(all_matchups, fp)
