import fasteners
import hashlib
import json
import logging
import os
import sys
import time
import timeit
import tqdm

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager


class TeamMappingsLoader:
    @staticmethod
    def load_team_mappings(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

class ProgressPrinter:
    @staticmethod
    def print_progress(current, total, away_team, home_team, book, league):
        progress = (current / total) * 100
        # Clear the line and print the progress bar with team names
        sys.stdout.write(f'\r{book}-{league} Progress: [{progress:>3.0f}%] {current}/{total} - ({away_team} @ {home_team})' + ' ' * 10)
        sys.stdout.flush()

class WebScraper:
    def __init__(self, league, book, team_mappings):
        self.league = league
        self.book = book
        self.live_games = 0
        self.total_games = 0
        self.team_mappings = team_mappings

    def encode_bet_table_id(self, matchup_id):
        return f'{self.book}_{matchup_id}'

    def encode_matchup_id(self, away_id, home_id):
        return f'{away_id}_{home_id}_{self.league}'

    def find_team_id(self, team_name):
        for team_mapping in self.team_mappings:
            if team_mapping["DraftKings Name"] == team_name:
                return team_mapping["TeamID"]
        return "Unknown"

    def find_abv(self, team_name):
        for team_mapping in self.team_mappings:
            if team_mapping["DraftKings Name"] == team_name:
                return team_mapping["PlainText"]
        return "Unknown"

    def find_team_rank_name(self, dk_team_name):
        for team_mapping in self.team_mappings:
            if team_mapping["DraftKings Name"] == dk_team_name:
                return team_mapping["Team Rankings Name"]
        return "Unknown"

    def find_element_text_or_not_found(self, driver, xpath, wait_time=2):
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, xpath))
            )
            if (element.text == ''):
                return '-999'
            return element.text
        except:
            return '-999'

    def scrape(self, driver, matchup_num):

        matchup_num *= 2
        x = matchup_num - 1  # Indicates Away Team
        y = matchup_num      # Indicates Home Team


        # Extract text for away and home teams, their spreads, money lines, total points, and start times using specific XPaths
        away_team_text = self.find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > th:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')
        home_team_text = self.find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({y}) > th:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)')
        away_spread_text = self.find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')
        away_spread_odds_text = self.find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')
        total_text = self.find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > td:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(3)')
        over_total_odds_text = self.find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > td:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')
        away_ml_text = self.find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > td:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)')
        home_spread_text = self.find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({y}) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')
        home_spread_odds_text = self.find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({y}) > td:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')
        under_total_odds_text = self.find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({y}) > td:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(1)')
        home_ml_text = self.find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({y}) > td:nth-child(4) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)')
        start_time_text = self.find_element_text_or_not_found(driver, f'.sportsbook-table__body > tr:nth-child({x}) > th:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2)')
        
        # Find team rank names and IDs using the extracted team names
        away_team_rank_name = self.find_team_rank_name(away_team_text)  # Name from team rankings.com
        home_team_rank_name = self.find_team_rank_name(home_team_text)  # Name from team rankings.com
        away_team_id = self.find_team_id(away_team_text)  # Team ID for away team
        home_team_id = self.find_team_id(home_team_text)  # Team ID for home team
        matchup_id = self.encode_matchup_id(away_team_id, home_team_id)
        bet_table_id = self.encode_bet_table_id(matchup_id)
        
        # Construct the information dictionary
        away_abv = self.find_abv(away_team_text)
        home_abv = self.find_abv(home_team_text)
        self.total_games += 1

        if (self.find_element_text_or_not_found(driver, f'div.parlay-card-10-a:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child({x}) > th:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > span:nth-child(2)') != '-999'):
            self.live_games += 1
            start_time_text = 'Live Game'

        # if start_time_text.__eq__('-999'):
        #     self.live_games += 1
        #     start_time_text = 'Live Game'
            
        info = [ 
            {
                'BetTableId': bet_table_id,
                'Odds Table': {
                    'Book Name': self.book, 
                    'Away Spread': away_spread_text, 
                    'Away Spread Odds': self.check_even(away_spread_odds_text),
                    'Away ML': self.check_even(away_ml_text),
                    'Home Spread': home_spread_text, 
                    'Home Spread Odds': self.check_even(home_spread_odds_text),
                    'Home ML': self.check_even(home_ml_text),
                    'Total': total_text,  # Remove the 'O/U' prefix from the total points text
                    'Over Total Odds': self.check_even(over_total_odds_text), 
                    'Under Total Odds': self.check_even(under_total_odds_text),
                },
                'MatchupID': matchup_id,
                'Info Table': {                
                        'Away Team': away_team_text, 
                        'Away Team Rank Name': away_team_rank_name,
                        'Away Abv': away_abv,
                        'Away ID': away_team_id,
                        'Home Team': home_team_text, 
                        'Home Team Rank Name': home_team_rank_name,
                        'Home Abv': home_abv,
                        'Home ID': home_team_id, 
                        'Start Time': start_time_text, 
                        'League': self.league
                    }
                }
            
        ]
        # Print the teams involved in the matchup for logging purposes
        #print(f'{away_team_text}, {home_team_text}')
        return info#, away_abv, home_abv
        # except Exception as e:
        #     print(f"Error scraping team {away_team_text}, {home_team_text}")
        #     return None
    
    def init_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('log-level=3')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    
    def check_even(self, text):
        if text == 'Even':
            return '+100'
        return text
    
    def read_games_count(self, game_type, data_file_path):
        with self.lock:
            if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
                with open(data_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    return data.get(game_type)
            return None  # Or appropriate error handling/alternative return value
       

    def scrape_all(self):

        driver = self.init_driver()
        driver.get("https://sportsbook.draftkings.com/leagues/basketball/nba")

        #Wait for table element to appear
        specific_tbody = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.parlay-card-10-a'))
        )

        num_rows = len(specific_tbody.find_elements(By.TAG_NAME, 'tr')) - 1 # Total number of teams playing today
        number_of_games = (num_rows) / 2 # Total number of games today
        all_matchups = [] # Empty container to store all matchup data

        for z in tqdm(range(1, int(number_of_games) + 1)):
            #print(f'{self.league} - {self.book}: {z}/{int(number_of_games)}')
            matchup = self.scrape(driver, z)
            #progress_printer.print_progress(z, int(number_of_games), away_team=away_team, home_team=home_team, book=self.book, league=self.league) # Print

            if matchup:
                all_matchups.append(matchup)

        driver.quit()
        return all_matchups

class DataUpdater:
    @staticmethod
    def update_games_count(data_file_path, game_type, number_of_games):
        with fasteners.InterProcessLock(data_file_path + '.lock'):
            if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
                with open(data_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            else:
                data = {}
            data[game_type] = number_of_games
            with open(data_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)

    @staticmethod
    def update_live_games_count(data_file_path, league, live_games):
        with fasteners.InterProcessLock(data_file_path + '.lock'):
            if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
                with open(data_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            else:
                data = {}
            data[league] = live_games
            with open(data_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)

def main():
    start = timeit.default_timer()

    webdriver.chrome
    logging.getLogger('scrapy').setLevel(logging.INFO)

    # Load team mappings
    team_mappings = TeamMappingsLoader.load_team_mappings('../../../Dictionary/Pro/NBA.json')

    # Initialize WebScraper
    scraper = WebScraper('NBA', 'DK', team_mappings)

    # Scraping and updating data
    all_matchups = scraper.scrape_all()
    DataUpdater.update_games_count('../games_count.json', scraper.league, scraper.total_games)
    DataUpdater.update_live_games_count('../live_games_count.json', scraper.league, scraper.live_games)

    # Writing to file
    try:
        with open('../../Data/DK/NBA.json', 'w', encoding='utf-8') as fp:
            json.dump(all_matchups, fp, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error writing to file: {e}")
    stop = timeit.default_timer()

    # print('Time: ', stop - start)  

if __name__ =='__main__':
    main()
