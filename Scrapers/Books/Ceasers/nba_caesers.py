import fasteners
import hashlib
import json
import logging
import os
import re
import sys
import time
import timeit

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from tqdm import tqdm 

class TeamMappingsLoader:
    @staticmethod
    def load_team_mappings(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
   
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
            if team_mapping["Full Name"] == team_name:
                return team_mapping["TeamID"]
        return "Unknown"

    def find_abv(self, team_name):
        for team_mapping in self.team_mappings:
            if team_mapping["Full Name"] == team_name:
                return team_mapping["PlainText"]
        return "Unknown"    
    
    def find_team_rank_name(self, team_name):
        for team_mapping in self.team_mappings:
            if team_mapping["Full Name"] == team_name:
                return team_mapping["Team Rankings Name"]
        return "Unknown" 
        
    def find_element_text_or_default(self, driver, xpath, wait_time=2):
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            if (element.text == ''):
                return '-999'
            return element.text
        except:
            return '-999'
        
        
    def check_even(text):
        """
        Checks if the provided text represents an 'Even' betting odd and converts it to a standard numerical format.

        In betting terminology, 'Even' odds mean that the potential win is the same amount as the stake. This function converts the textual representation 'Even' to its numerical equivalent '+100', which is the standard format used in betting to represent even odds. If the text does not represent 'Even' odds, it is returned unchanged.

        Parameters:
        - text (str): The text to check for 'Even' odds.

        Returns:
        - str: Returns '+100' if the input text is 'Even', otherwise returns the original text.
        """
        if text == 'EVEN':
            return '+100'
        return text

    def scrape_live(self, driver, matchup_num):
        """
        Scrapes betting information for a specific matchup from a webpage.

        This function navigates to specific elements on a webpage using XPath to extract information about a sports matchup. It retrieves details such as team names, spread values, moneyline (ML) values, total points, and start times. It then uses helper functions to find additional information like team rankings and IDs based on the scraped team names. Finally, it compiles all the information into a structured dictionary.

        Parameters:
        - matchup_num (int): The number of the matchup on the webpage, used to construct the XPath for locating elements.

        Returns:
        - list: A list containing a single dictionary with detailed betting and matchup information, including team names, IDs, rankings, and betting odds.
        """
        # Scraping various pieces of information using XPath. Each piece corresponds to a specific betting or game detail.
        away_team_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-happening-now/div/div/div/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/header/sp-competitor-coupon/a/div[1]/h4[1]/span[1]')
        home_team_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-happening-now/div/div/div/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/header/sp-competitor-coupon/a/div[1]/h4[2]/span[1]')
        away_spread_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-happening-now/div/div/div/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[1]/ul/li[1]/sp-outcome/button/sp-spread-outcome/span')
        away_spread_odds_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-happening-now/div/div/div/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[1]/ul/li[1]/sp-outcome/button/span[1]')
        total_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-happening-now/div/div/div/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[3]/ul/li[1]/sp-outcome/button/sp-total-outcome/span[2]')
        over_total_odds_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-happening-now/div/div/div/div/sp-coupon/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[3]/ul/li[1]/sp-outcome/button/span[1]')
        away_ml_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-happening-now/div/div/div/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[2]/ul/li[1]/sp-outcome/button/span[1]')
        home_spread_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-happening-now/div/div/div/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[1]/ul/li[1]/sp-outcome/button/sp-spread-outcome/span')
        home_spread_odds_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-happening-now/div/div/div/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[1]/ul/li[2]/sp-outcome/button/span[1]')
        under_total_odds_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-happening-now/div/div/div/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[3]/ul/li[2]/sp-outcome/button/span[1]')
        home_ml_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-happening-now/div/div/div/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[2]/ul/li[2]/sp-outcome/button/span[1]')
        start_time_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-happening-now/div/div/div/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-score-coupon/span/span')
        
        # Using helper functions to find team rankings and IDs based on the scraped team names.
        away_team_rank_name = self.find_team_rank_name(away_team_text)  # Name from team rankings.com
        home_team_rank_name = self.find_team_rank_name(home_team_text)  # Name from team rankings.com
        away_team_id = self.find_team_id(away_team_text)  # Team
        home_team_id = self.find_team_id(home_team_text)  # Team
        
        # Generating unique identifiers for the matchup and the betting table.
        matchup_id = self.encode_matchup_id(away_team_id, home_team_id)
        bet_table_id = self.encode_bet_table_id(matchup_id, self.book)
        away_abv = self.find_abv(away_team_text)
        home_abv = self.find_abv(home_team_text)
        
            
        info = [ 
            {
                'BetTableId': bet_table_id,
                'Odds Table': {
                    'Book Name': self.book, 
                    'Away Spread': away_spread_text, 
                    'Away Spread Odds': self.check_even(away_spread_odds_text[1:-1]),
                    'Away ML': self.check_even(away_ml_text),
                    'Home Spread': home_spread_text, 
                    'Home Spread Odds': self.check_even(home_spread_odds_text[1:-1]),
                    'Home ML': self.check_even(home_ml_text),
                    'Total': total_text, 
                    'Over Total Odds': self.check_even(over_total_odds_text[1:-1]), 
                    'Under Total Odds': self.check_even(under_total_odds_text[1:-1]),
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
        
        # Printing the teams involved in the matchup for logging purposes.
        #print(f'{away_team_text}, {home_team_text}')
        return info

    def scrape(self, driver, matchup_num):
        """
        Scrapes betting information for a specific matchup from a webpage.

        This function navigates to specific elements on a webpage using XPath to extract information about a sports matchup. It retrieves details such as team names, spread values, moneyline (ML) values, total points, and start times. It then uses helper functions to find additional information like team rankings and IDs based on the scraped team names. Finally, it compiles all the information into a structured dictionary.

        Parameters:
        - matchup_num (int): The number of the matchup on the webpage, used to construct the XPath for locating elements.

        Returns:
        - list: A list containing a single dictionary with detailed betting and matchup information, including team names, IDs, rankings, and betting odds.
        """
        # Scraping various pieces of information using XPath. Each piece corresponds to a specific betting or game detail.
        away_team_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/header/sp-competitor-coupon/a/div[1]/h4[1]/span[1]')
        home_team_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/header/sp-competitor-coupon/a/div[1]/h4[2]/span[1]')
        away_spread_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[1]/ul/li[1]/sp-outcome/button/sp-spread-outcome/span')
        away_spread_odds_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[1]/ul/li[1]/sp-outcome/button/span[1]')
        total_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[3]/ul/li[1]/sp-outcome/button/sp-total-outcome/span[2]')
        over_total_odds_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[3]/ul/li[1]/sp-outcome/button/span[1]')
        away_ml_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[2]/ul/li[1]/sp-outcome/button/span[1]')
        home_spread_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[1]/ul/li[2]/sp-outcome/button/sp-spread-outcome/span')
        home_spread_odds_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[1]/ul/li[2]/sp-outcome/button/span[1]')
        under_total_odds_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[3]/ul/li[2]/sp-outcome/button/span[1]')
        home_ml_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[2]/ul/li[2]/sp-outcome/button/span[1]')
        start_time_text = self.find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-score-coupon/span/time')
        
        # Using helper functions to find team rankings and IDs based on the scraped team names.
        away_team_rank_name = self.find_team_rank_name(away_team_text)  # Name from team rankings.com
        home_team_rank_name = self.find_team_rank_name(home_team_text)  # Name from team rankings.com
        away_team_id = self.find_team_id(away_team_text)  # Team
        home_team_id = self.find_team_id(home_team_text)  # Team
        
        # Generating unique identifiers for the matchup and the betting table.
        matchup_id = self.encode_matchup_id(away_team_id, home_team_id)
        bet_table_id = self.encode_bet_table_id(matchup_id, self.book)
        
        # Compiling all the scraped and generated information into a structured dictionary.
        away_abv = self.find_abv(away_team_text)
        home_abv = self.find_abv(home_team_text)

        info = [ 
            {
                'BetTableId': bet_table_id,
                'Odds Table': {
                    'Book Name': self.book, 
                    'Away Spread': away_spread_text, 
                    'Away Spread Odds': self.check_even(away_spread_odds_text[1:-1]),
                    'Away ML': self.check_even(away_ml_text),
                    'Home Spread': home_spread_text, 
                    'Home Spread Odds': self.check_even(home_spread_odds_text[1:-1]),
                    'Home ML': self.check_even(home_ml_text),
                    'Total': total_text, 
                    'Over Total Odds': self.check_even(over_total_odds_text[1:-1]), 
                    'Under Total Odds': self.check_even(under_total_odds_text[1:-1]),
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
        
        # Printing the teams involved in the matchup for logging purposes.
        #print(f'{away_team_text}, {home_team_text}')
        return info

    def init_driver(self):
        options = Options()
        #options.add_argument('--headless')
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

    def read_live_games(self, game_type, data_file_path):
        with self.lock:
            if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
                with open(data_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    return data.get(game_type)
            return None  # Or appropriate error handling/alternative return value

    def scrape_nba(self, driver, matchup_num):        
        matchup_num += 1

        away_team_text = self.find_element_text_or_default(driver, f'/html/body/div[2]/div/div[19]/div/div[1]/div/div/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[{matchup_num}]/div/div/div[1]/a[1]/div/div/div[2]/div/span')
        away_spread_text = self.find_element_text_or_default(driver, f'/html/body/div[2]/div/div[19]/div/div[1]/div/div/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[{matchup_num}]/div/div/div[1]/div[6]/button/div/div[1]/div/div')
        away_spread_odds = self.find_element_text_or_default(driver, f'/html/body/div[2]/div/div[19]/div/div[1]/div/div/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[{matchup_num}]/div/div/div/div[6]/button/div/div[2]')
        away_ml = self.find_element_text_or_default(driver, f'/html/body/div[2]/div/div[19]/div/div[1]/div/div/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[{matchup_num}]/div/div/div[1]/div[3]/button/div/div')
        
        home_team_text = self.find_element_text_or_default(driver, f'/html/body/div[2]/div/div[19]/div/div[1]/div/div/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[{matchup_num}]/div/div/div[1]/a[2]/div/div/div[2]/div/span')
        home_spread_text = self.find_element_text_or_default(driver, f'/html/body/div[2]/div/div[19]/div/div[1]/div/div/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[{matchup_num}]/div/div/div[1]/div[7]/button/div/div[1]/div/div')
        home_spread_odds = self.find_element_text_or_default(driver, f'/html/body/div[2]/div/div[19]/div/div[1]/div/div/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[{matchup_num}]/div/div/div/div[7]/button/div/div[2]')
        home_ml = self.find_element_text_or_default(driver, f'/html/body/div[2]/div/div[19]/div/div[1]/div/div/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[{matchup_num}]/div/div/div[1]/div[4]/button/div/div')

        total_text = self.find_element_text_or_default(driver, f'/html/body/div[2]/div/div[19]/div/div[1]/div/div/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[{matchup_num}]/div/div/div[1]/div[9]/button/div/div[1]/div/div')
        over_total = self.find_element_text_or_default(driver, f'/html/body/div[2]/div/div[19]/div/div[1]/div/div/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[{matchup_num}]/div/div/div[1]/div[9]/button/div/div[2]')
        under_total = self.find_element_text_or_default(driver, f'/html/body/div[2]/div/div[19]/div/div[1]/div/div/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[{matchup_num}]/div/div/div[1]/div[10]/button/div/div[2]')

        #matchup_id = self.encode_matchup_id(away_team_id, home_team_id)

        # Running these before swapping elements somehow works
        away_team_rank_name = self.find_team_rank_name(away_team_text)  # Name from team rankings.com
        home_team_rank_name = self.find_team_rank_name(home_team_text) 
        

        
        # Check if matchup_num is odd, if so reverse home and away teams; 
        # Caesers ain't smarter than me nice try tho. 
        # Ok maybe they are 
        if matchup_num % 2 != 0:
            # Swap home and away data
            temp_team = home_team_text
            home_team_text = away_team_text
            away_team_text = temp_team

            temp_spread_text = home_spread_text
            home_spread_text = away_spread_text
            away_spread_text = temp_spread_text

            temp_spread_odds = home_spread_odds
            home_spread_odds = away_spread_odds
            away_spread_odds = temp_spread_odds
            
            # temp_ml = home_ml
            # home_ml = away_ml #They swap everything but the home and away ml on odd matchups, interesting.
            # away_ml = home_ml
            
            temp_total = over_total
            over_total = under_total
            under_total = temp_total
    

    
        away_team_id = self.find_team_id(away_team_text)  # Team
        home_team_id = self.find_team_id(home_team_text)  # Team
        
        
        # Using helper functions to find team rankings and IDs based on the scraped team names.
 # Name from team rankings.com
        # away_team_id = self.find_team_id(away_team_text)  # Team
        # home_team_id = self.find_team_id(home_team_text)  # Team
        
        # # Generating unique identifiers for the matchup and the betting table.
        # bet_table_id = self.encode_bet_table_id(matchup_id, self.book)
        # away_abv = self.find_abv(away_team_text)
        # home_abv = self.find_abv(home_team_text)
        
            
        #Testing ml 
        test = self.find_element_text_or_default(driver, f'/html/body/div[2]/div/div[19]/div/div[1]/div/div/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[5]/div/div/div/div[3]/button/div/div')
        #print(f'TEST:{test}')

        
        print(f'Game: {matchup_num}, Away:{away_team_id}, Away Team:{away_team_text}')
        #print(home_abv, away_abv, matchup_id, bet_table_id)
        #test output
        # print(away_team_text, away_ml, away_spread_text, away_spread_odds, total_text[2:], over_total)
        # print('@')
        # print(home_team_text, home_ml, home_spread_text, home_spread_odds, total_text[2:], under_total)
        #print(f'{away_team_text}: {away_ml} \n {home_team_text}: {home_ml}')
        
            
    def scrape_all(self):
        
        driver = self.init_driver()
        driver.get("https://sportsbook.caesars.com/us/wa-ms/bet?dl=retail_mode")
        time.sleep(4)  # Allow some time for the page to load JavaScript content

        data_file_path = '../games_count.json'
        lock_file_path = '../games_count.lock'
        self.lock = fasteners.InterProcessLock(lock_file_path)

        number_of_games = self.read_games_count('NBA', data_file_path)

        data_file_path = '../live_games_count.json'
        lock_file_path = '../live_games_count.lock'

        live_games = self.read_live_games('NBA', data_file_path)

        # number_of_games = 0
        # number_of_games_text = self.find_element_text_or_default(driver, '/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/h4/button')
        # match = re.search(r'\((\d+)\)', number_of_games_text)

        # if match: number_of_games = (int(match.group(1)))

        upcoming_games = int(number_of_games) - int(live_games)

        all_matchups = []

        for z in (range(1, int(4)+1)):
            matchup = self.scrape_nba(driver, z)
            if matchup:
                all_matchups.append(matchup)


        driver.quit()
        return all_matchups

def main():
    start = timeit.default_timer()

    webdriver.chrome
    logging.getLogger('scrapy').setLevel(logging.INFO)

    # Load team mappings
    team_mappings = TeamMappingsLoader.load_team_mappings('../../../Dictionary/Pro/NBA.json')

    scraper = WebScraper('NBA', 'Full Name', team_mappings)
    all_matchups = scraper.scrape_all()

    try:
        with open('../../Data/Caesers/NBA.json', 'w', encoding='utf-8') as fp:
            json.dump(all_matchups, fp, indent=4)
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == '__main__':
    main()
