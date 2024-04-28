import fasteners
import hashlib
import json
import logging
import os
import sys
import time
import timeit

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm


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
        self.team_mappings = team_mappings

    def encode_bet_table_id(self, matchup_id, book_name):
        if matchup_id and book_name:
            return f'{self.book}_{matchup_id}'
        return "Unknown" 
    
    def encode_matchup_id(self, away_id, home_id):
        if away_id and home_id:
            return f'{away_id}_{home_id}_{self.league}'
        return "Unknown"
    
    def find_team_id(self, team_name):
        for team_mapping in self.team_mappings:
            if team_mapping["ESPNBet"] == team_name:
                return team_mapping["TeamID"]
        return "Unknown"

    def find_abv(self, team_name):
        for team_mapping in self.team_mappings:
            if team_mapping["ESPNBet"] == team_name:
                return team_mapping["PlainText"]
        return "Unknown"    
    
    def find_team_rank_name(self, team_name):
        for team_mapping in self.team_mappings:
            if team_mapping["ESPNBet"] == team_name:
                return team_mapping["Team Rankings Name"]
        return "Unknown" 
        
    def find_element_text_or_not_found(self, driver, xpath, wait_time=3):
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            if (element.text == ''):
                return '-999'
            return element.text
        except:
            return '-999'
        
    def scrape(self, driver, matchup_num):
        # Extract text for various betting elements using XPath and the provided matchup number
        away_team_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[1]/button/div/div/div[1]')
        home_team_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[1]/button/div/div/div[1]')
        away_spread_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[1]/span[1]')
        away_spread_odds_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[1]/span[2]')
        total_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[2]/span[1]')
        over_total_odds_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[2]/span[2]')
        away_ml_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[3]/span[2]')
        home_spread_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[2]/button[1]/span[1]')
        home_spread_odds_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[2]/button[1]/span[2]')
        under_total_odds_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[2]/button[2]/span[2]')
        home_ml_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[2]/button[3]/span[2]')
        start_time_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[1]/button/span[1]')

        # Use other functions to find team rank names and IDs based on the scraped team names
        away_team_rank_name = self.find_team_rank_name(away_team_text)  # Name from team rankings.com
        home_team_rank_name = self.find_team_rank_name(home_team_text)  # Name from team rankings.com
        away_team_id = self.find_team_id(away_team_text)  # Team ID for away team
        home_team_id = self.find_team_id(home_team_text)  # Team ID for home team

        # Generate unique identifiers for the matchup and the betting table
        matchup_id = self.encode_matchup_id(away_team_id, home_team_id)
        bet_table_id = self.encode_bet_table_id(matchup_id, self.book)
        away_abv = self.find_abv(away_team_text)
        home_abv = self.find_abv(home_team_text)

        if start_time_text.__eq__('-999'):
            # self.live_games += 1
            start_time_text = 'Live Game'
           

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
                    'Total': total_text[2:],  # Remove the 'O/U' prefix from the total points text
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
        return info, away_abv, home_abv
    
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
        driver.get("https://espnbet.com/sport/baseball/organization/united-states/competition/mlb/featured-page")
        time.sleep(1)

        data_file_path = '../games_count.json'
        lock_file_path = '../games_count.lock'
        self.lock = fasteners.InterProcessLock(lock_file_path)

        number_of_games = self.read_games_count('MLB', data_file_path)
        all_matchups = []

#        progress_printer = ProgressPrinter()
#        progress_printer.print_progress(0, int(number_of_games), away_team='Away Team', home_team='Home Team', book=self.book, league=self.league)

        for z in tqdm(range(1, int(number_of_games)+1)):
            # print(f'{self.league} - {self.book}: {z}/{int(number_of_games)}')
            #matchup = self.scrape(driver, z)
            matchup, away_team, home_team = self.scrape(driver, z)
            #progress_printer.print_progress(z, int(number_of_games), away_team=away_team, home_team=home_team, book=self.book, league=self.league) # Print


            if matchup:
                all_matchups.append(matchup)

        #print(f'Total matchups scraped: {len(all_matchups)}')

        driver.quit()
        return all_matchups

def main():
    start = timeit.default_timer()

    webdriver.chrome
    logging.getLogger('scrapy').setLevel(logging.INFO)

    # Load team mappings
    team_mappings = TeamMappingsLoader.load_team_mappings('../../../Dictionary/Pro/MLB.json')

    scraper = WebScraper('MLB', 'ESPN', team_mappings)
    all_matchups = scraper.scrape_all()

    try:
        with open('../../Data/ESPN/MLB.json', 'w', encoding='utf-8') as fp:
            json.dump(all_matchups, fp, indent=4)
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == '__main__':
    main()