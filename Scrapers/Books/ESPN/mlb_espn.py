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
        
    def find_element_text_or_not_found(self, driver, xpath, wait_time=1):
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

        progress_printer = ProgressPrinter()
        progress_printer.print_progress(0, int(number_of_games), away_team='Away Team', home_team='Home Team', book=self.book, league=self.league)

        for z in range(1, int(number_of_games)+1):
            # print(f'{self.league} - {self.book}: {z}/{int(number_of_games)}')
            # matchup = self.scrape(driver, z)
            matchup, away_team, home_team = self.scrape(driver, z)
            progress_printer.print_progress(z, int(number_of_games), away_team=away_team, home_team=home_team, book=self.book, league=self.league) # Print


            if matchup:
                all_matchups.append(matchup)

        #print(f'Total matchups scraped: {len(all_matchups)}')

        driver.quit()
        return all_matchups


        #Writes to JSON

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

# league = 'MLB'
# book = 'ESPN'

# with open('../../../Dictionary/Pro/MLB.json', 'r', encoding='utf-8') as file:
#     team_mappings = json.load(file)

# def encode_bet_table_id(matchup_id, book_name):
#     """
#     Generates a unique identifier for a betting table based on the matchup ID and the book name.

#     Parameters:
#     - matchup_id (str): The unique identifier for the matchup.
#     - book_name (str): The name of the bookmaker.

#     Returns:
#     - str: A string that combines the book name and the matchup ID, separated by an underscore.
#           Returns "Unknown" if either the matchup_id or book_name is missing.
#     """
#     if matchup_id and book_name:
#         return f'{book_name}_{matchup_id}'
#     return "Unknown" 

# def encode_matchup_id(away_id, home_id, league):
#     """
#     Generates a unique identifier for a matchup based on the IDs of the away and home teams, along with the league.

#     Parameters:
#     - away_id (str): The unique identifier for the away team.
#     - home_id (str): The unique identifier for the home team.
#     - league (str): The name of the league in which the matchup occurs.

#     Returns:
#     - str: A string that combines the away team ID, home team ID, and league, separated by underscores.
#           Returns "Unknown" if either the away_id or home_id is missing.
#     """
#     if away_id and home_id:
#         return f'{away_id}_{home_id}_{league}'
#     return "Unknown"

# def find_team_id(team_name):
#     """
#     Searches for a team's ID based on its name in a predefined list of team mappings.

#     Parameters:
#     - team_name (str): The name of the team for which the ID is being searched.

#     Returns:
#     - str: The ID of the team if found in the team mappings; otherwise, returns "Unknown".
#     """
#     for team_mapping in team_mappings:
#         if team_mapping["ESPNBet"] == team_name:
#             return team_mapping["TeamID"]
#     return "Unknown"  # Return a default value if the team name is not found in the mappings  # Return a default value if not found

# def find_abv(team_name):
#     """
#     Searches for a team's ID based on its name from a predefined list of team mappings.

#     Parameters:
#     - team_name (str): The name of the team as recognized by DraftKings.

#     Returns:
#     - str: The unique TeamID associated with the given team name. Returns "Unknown" if the team name is not found in the mappings.
#     """
#     for team_mapping in team_mappings:
#         if team_mapping["ESPNBet"] == team_name:
#             return team_mapping["PlainText"]
#     return "Unknown"  # Return a default value if not found

# def find_team_rank_name(dk_team_name):
#     """
#     Searches for a team's ranking name based on its name in a predefined list of team mappings.

#     This function iterates through a global list of team mappings, looking for a match between the provided team name
#     and the 'ESPNBet' key in each mapping. If a match is found, it returns the 'Team Rankings Name' associated with that team.
#     If no match is found, it returns "Unknown".

#     Parameters:
#     - dk_team_name (str): The name of the team for which the ranking name is being searched.

#     Returns:
#     - str: The ranking name of the team if found in the team mappings; otherwise, returns "Unknown".
#     """
#     for team_mapping in team_mappings:
#         if team_mapping["ESPNBet"] == dk_team_name:
#             return team_mapping["Team Rankings Name"]
#     return "Unknown"  # Return a default value if the team name is not found in the mappings  # Return a default value if not found

# def scrape(self, driver, matchup_num):
#     # Extract text for various betting elements using XPath and the provided matchup number
#     away_team_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[1]/button/div/div/div[1]')
#     home_team_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[1]/button/div/div/div[1]')
#     away_spread_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[1]/span[1]')
#     away_spread_odds_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[1]/span[2]')
#     total_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[2]/span[1]')
#     over_total_odds_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[2]/span[2]')
#     away_ml_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[3]/span[2]')
#     home_spread_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[2]/button[1]/span[1]')
#     home_spread_odds_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[2]/button[1]/span[2]')
#     under_total_odds_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[2]/button[2]/span[2]')
#     home_ml_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[2]/button[3]/span[2]')
#     start_time_text = self.find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[1]/button/span[1]')

#     # Use other functions to find team rank names and IDs based on the scraped team names
#     away_team_rank_name = self.find_team_rank_name(away_team_text)  # Name from team rankings.com
#     home_team_rank_name = self.find_team_rank_name(home_team_text)  # Name from team rankings.com
#     away_team_id = self.find_team_id(away_team_text)  # Team ID for away team
#     home_team_id = self.find_team_id(home_team_text)  # Team ID for home team

#     # Generate unique identifiers for the matchup and the betting table
#     matchup_id = self.encode_matchup_id(away_team_id, home_team_id, league)
#     bet_table_id = self.encode_bet_table_id(matchup_id, book)

#     # Construct the information dictionary for the matchup
#     away_abv = self.find_abv(away_team_text)
#     home_abv = self.find_abv(home_team_text)

        
#     info = [ 
#         {
#             'BetTableId': bet_table_id,
#             'Odds Table': {
#                 'Book Name': book, 
#                 'Away Spread': away_spread_text, 
#                 'Away Spread Odds': check_even(away_spread_odds_text),
#                 'Away ML': check_even(away_ml_text),
#                 'Home Spread': home_spread_text, 
#                 'Home Spread Odds': check_even(home_spread_odds_text),
#                 'Home ML': check_even(home_ml_text),
#                 'Total': total_text[2:],  # Remove the 'O/U' prefix from the total points text
#                 'Over Total Odds': check_even(over_total_odds_text), 
#                 'Under Total Odds': check_even(under_total_odds_text),
#             },
#             'MatchupID': matchup_id,
#             'Info Table': {                
#                     'Away Team': away_team_text, 
#                     'Away Team Rank Name': away_team_rank_name,
#                     'Away Abv': away_abv,
#                     'Away ID': away_team_id,
#                     'Home Team': home_team_text, 
#                     'Home Team Rank Name': home_team_rank_name,
#                     'Home Abv': home_abv,
#                     'Home ID': home_team_id, 
#                     'Start Time': start_time_text, 
#                     'League': league
#                 }
#             }
        
#     ]

#     # Print the teams involved in the matchup for logging purposes
#     print(f'{away_team_text}, {home_team_text}')
#     return info

#     def init_driver(self):
#         options = Options()
#         options.add_argument('--headless')
#         options.add_argument('log-level=3')

#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=options)
#         return driver
    
#     def scrape_all(self):
        
#         driver = self.init_driver()
#         driver.get("https://espnbet.com/sport/baseball/organization/united-states/competition/mlb/featured-page")
#         time.sleep(1)

#         data_file_path = '../games_count.json'
#         lock_file_path = '../games_count.lock'
#         lock = fasteners.InterProcessLock(lock_file_path)

#         number_of_games = read_games_count('MLB')
#         all_matchups = []

#         progress_printer = ProgressPrinter()
#         progress_printer.print_progress(0, int(number_of_games), away_team='Away Team', home_team='Home Team', book=self.book, league=self.league)

#         for z in range(1, int(number_of_games)+1):
#             print(f'{league} - {book}: {z}/{int(number_of_games)}')
#             matchup = scrape(z)
#             if matchup:
#                 all_matchups.append(matchup)

#         print(f'Total matchups scraped: {len(all_matchups)}')

#         driver.quit()
#         return all_matchups


#         #Writes to JSON




# # def main():
# #     start = timeit.default_timer()

# #     webdriver.chrome
# #     logging.getLogger('scrapy').setLevel(logging.INFO)

# #     # Load team mappings
# #     team_mappings = TeamMappingsLoader.load_team_mappings('../../../Dictionary/Pro/MLB.json')

# #     scraper = WebScraper('MLB', 'ESPN', team_mappings)
# #     all_matchups = scraper.scrape_all()

# #     try:
# #         with open('../../Data/ESPN/MLB.json', 'w', encoding='utf-8') as fp:
# #             json.dump(all_matchups, fp, indent=4)
# #     except Exception as e:
# #         print(f"Error writing to file: {e}")

# # match = {}

# # def clean_team(raw_team):
# #     """
# #     Cleans and formats the team name extracted from raw data.

# #     This function takes a raw team name string, splits it by spaces, and selects the second part (assuming the first part is not needed).
# #     It then converts this part to uppercase. If the team name is 'TRAIL', it corrects it to 'TRAILBLAZERS' to handle a specific case.

# #     Parameters:
# #     - raw_team (str): The raw team name string to be cleaned.

# #     Returns:
# #     - str: The cleaned and formatted team name.
# #     """
# #     team = raw_team.split(" ")
# #     team = team[1].upper()
# #     if team == 'TRAIL':
# #         team = 'TRAILBLAZERS'
# #     return team

# # def generate_game_id(away_team, home_team):
# #     """
# #     Generates a unique game identifier using MD5 hashing.

# #     This function takes the names of the away and home teams, concatenates them, and then applies MD5 hashing to the combined string to generate a unique identifier for the game. This identifier can be used to distinguish games in databases or logs where unique identification of each game is required.

# #     Parameters:
# #     - away_team (str): The name of the away team.
# #     - home_team (str): The name of the home team.

# #     Returns:
# #     - str: A hexadecimal string representing the MD5 hash of the concatenated team names, serving as a unique identifier for the game.
# #     """
# #     combined_string = away_team + home_team
# #     hash_object = hashlib.md5(combined_string.encode())
# #     return hash_object.hexdigest()

# # def find_element_text_or_not_found(driver, xpath, wait_time=2):
# #     """
# #     Attempts to find an element on a web page using its XPath and returns its text. If the element is not found within the specified wait time, returns 'N/A'.

# #     Parameters:
# #     - driver: The Selenium WebDriver instance used to interact with the web page.
# #     - xpath (str): The XPath string used to locate the element on the web page.
# #     - wait_time (int, optional): The maximum number of seconds to wait for the element to become visible. Defaults to 10 seconds.

# #     Returns:
# #     - str: The text of the found element, or 'N/A' if the element is not found within the specified wait time.
# #     """
# #     try:
# #         element = WebDriverWait(driver, wait_time).until(
# #             EC.visibility_of_element_located((By.XPATH, xpath))
# #         )
# #         if (element.text == ''):
# #             return 'N/A'
# #         return element.text
# #     except:
# #         return 'N/A'

# # #Espn has +100 odds set to 'Even'
# # def check_even(text):
# #     """
# #     Checks if the provided text represents an 'Even' betting odd and converts it to a standard numerical format.

# #     In betting terminology, 'Even' odds mean that the potential win is the same amount as the stake. This function
# #     translates 'Even' to '+100', which is the standard numerical representation for even odds in betting. If the input
# #     text is not 'Even', it returns the text unchanged.

# #     Parameters:
# #     - text (str): The text representing betting odds.

# #     Returns:
# #     - str: A string '+100' if the input is 'Even', otherwise returns the original text.
# #     """
# #     if text == 'Even':
# #         return '+100'
# #     return text

# # def scrape(matchup_num):
# #     """
# #     Scrapes betting information for a specific matchup from a webpage using Selenium.

# #     This function navigates to specific elements on a webpage using XPath to extract information about a sports matchup,
# #     including team names, spreads, money lines, and total points. It constructs a dictionary containing all the scraped
# #     data, including identifiers generated by other functions in the script.

# #     Parameters:
# #     - matchup_num (int): The number of the matchup on the webpage, used to construct the XPath for locating elements.

# #     Returns:
# #     - list: A list containing a single dictionary with the scraped data for the matchup, including betting odds,
# #             team information, and unique identifiers for the matchup and betting table.
# #     """
# #     # Extract text for various betting elements using XPath and the provided matchup number
# #     away_team_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[1]/button/div/div/div[1]')
# #     home_team_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[1]/button/div/div/div[1]')
# #     away_spread_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[1]/span[1]')
# #     away_spread_odds_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[1]/span[2]')
# #     total_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[2]/span[1]')
# #     over_total_odds_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[2]/span[2]')
# #     away_ml_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[2]/div[2]/button[3]/span[2]')
# #     home_spread_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[2]/button[1]/span[1]')
# #     home_spread_odds_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[2]/button[1]/span[2]')
# #     under_total_odds_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[2]/button[2]/span[2]')
# #     home_ml_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[3]/div[2]/button[3]/span[2]')
# #     start_time_text = find_element_text_or_not_found(driver, f'/html/body/div/div/div[2]/main/div[2]/div[3]/div/div/section/div[2]/article[{matchup_num}]/div/div[1]/button/span[1]')

# #     # Use other functions to find team rank names and IDs based on the scraped team names
# #     away_team_rank_name = find_team_rank_name(away_team_text)  # Name from team rankings.com
# #     home_team_rank_name = find_team_rank_name(home_team_text)  # Name from team rankings.com
# #     away_team_id = find_team_id(away_team_text)  # Team ID for away team
# #     home_team_id = find_team_id(home_team_text)  # Team ID for home team

# #     # Generate unique identifiers for the matchup and the betting table
# #     matchup_id = encode_matchup_id(away_team_id, home_team_id, league)
# #     bet_table_id = encode_bet_table_id(matchup_id, book)

# #     # Construct the information dictionary for the matchup
# #     away_abv = find_abv(away_team_text)
# #     home_abv = find_abv(home_team_text)

        
# #     info = [ 
# #         {
# #             'BetTableId': bet_table_id,
# #             'Odds Table': {
# #                 'Book Name': book, 
# #                 'Away Spread': away_spread_text, 
# #                 'Away Spread Odds': check_even(away_spread_odds_text),
# #                 'Away ML': check_even(away_ml_text),
# #                 'Home Spread': home_spread_text, 
# #                 'Home Spread Odds': check_even(home_spread_odds_text),
# #                 'Home ML': check_even(home_ml_text),
# #                 'Total': total_text[2:],  # Remove the 'O/U' prefix from the total points text
# #                 'Over Total Odds': check_even(over_total_odds_text), 
# #                 'Under Total Odds': check_even(under_total_odds_text),
# #             },
# #             'MatchupID': matchup_id,
# #             'Info Table': {                
# #                     'Away Team': away_team_text, 
# #                     'Away Team Rank Name': away_team_rank_name,
# #                     'Away Abv': away_abv,
# #                     'Away ID': away_team_id,
# #                     'Home Team': home_team_text, 
# #                     'Home Team Rank Name': home_team_rank_name,
# #                     'Home Abv': home_abv,
# #                     'Home ID': home_team_id, 
# #                     'Start Time': start_time_text, 
# #                     'League': league
# #                 }
# #             }
        
# #     ]

# #     # Print the teams involved in the matchup for logging purposes
# #     print(f'{away_team_text}, {home_team_text}')
# #     return info

# # def scrape_with_timeout(z, timeout=4):
# #     """
# #     Attempts to scrape betting information for a specific matchup with a timeout limit.
    
# #     This function initiates a separate thread to perform the scraping operation to avoid blocking the main thread.
# #     If the scraping operation exceeds the specified timeout, the operation is aborted, and the WebDriver is quit to
# #     release resources. This approach ensures that the scraping process does not hang indefinitely.
    
# #     Parameters:
# #     - z (int): The number of the matchup to scrape. This number is used to identify specific elements on the webpage.
# #     - timeout (int, optional): The maximum number of seconds to wait for the scraping operation to complete. Defaults to 7 seconds.
    
# #     Returns:
# #     - list or None: A list containing a single dictionary with the scraped data for the matchup if the operation completes
# #                     within the timeout period; otherwise, None if the operation times out.
# #     """
# #     # This will hold the result of the scrape function
# #     result = [None]
    
# #     def target():
# #         """
# #         Target function to be executed by the thread.
        
# #         Calls the scrape function and stores the result in a nonlocal list to make it accessible outside the nested function.
# #         """
# #         # Call the scrape function and store the result in the nonlocal list
# #         result[0] = scrape(z)
        
# #     # Set up the thread to run the scrape function
# #     thread = threading.Thread(target=target)
# #     thread.start()
# #     thread.join(timeout)  # Wait for the time limit
# #     if thread.is_alive():
# #         print(f"Scraping took too long, moving on to the next matchup.")
# #         driver.quit()  # Quit the WebDriver to release resources
# #         return None  # Ensure the thread has finished before returning
        
# #     return result[0]


# # def read_games_count(game_type):
# #     """
# #     Reads the count of games for a specified game type from a JSON file.

# #     This function attempts to read a JSON file specified by the global variable `data_file_path`. It acquires a lock
# #     before accessing the file to ensure thread-safe and process-safe operations in a concurrent environment. The function
# #     looks for the game count associated with the provided `game_type` key in the JSON data. If the file does not exist,
# #     is empty, or the `game_type` key is not found, the function returns None.

# #     Parameters:
# #     - game_type (str): The type of game for which the count is being requested. This acts as a key in the JSON data structure.

# #     Returns:
# #     - int or None: The count of games for the specified `game_type` if found; otherwise, None.
# #     """
# #     with lock:
# #         if os.path.exists(data_file_path) and os.path.getsize(data_file_path) > 0:
# #             with open(data_file_path, 'r', encoding='utf-8') as file:
# #                 data = json.load(file)
# #                 return data.get(game_type)
# #         return None  # Or appropriate error handling/alternative return value


# # options = Options()
# # options.add_argument('--headless')
# # options.add_argument('log-level=3')

# # # Initialize the Service
# # service = Service(ChromeDriverManager().install())

# # # Initialize WebDriver without the 'desired_capabilities' argument
# # driver = webdriver.Chrome(service=service, options=options)


# # driver = self.init_driver()
# # driver.get("https://espnbet.com/sport/baseball/organization/united-states/competition/mlb/featured-page")


# # time.sleep(3)  # Reduced sleep time after initial load
# # #specific_tbody = driver.find_element(By.CSS_SELECTOR, 'tbody.sportsbook-table__body')

# # #num_rows = len(specific_tbody.find_elements(By.TAG_NAME, 'tr'))

# # #number_of_games = 14# num_rows/2
# # #all_matchups = []
# # #z = 15  # Start with the first matchup



# # data_file_path = '../games_count.json'
# # lock_file_path = '../games_count.lock'
# # lock = fasteners.InterProcessLock(lock_file_path)


# # number_of_games = read_games_count('MLB')
# # all_matchups = []
# # for z in range(1, int(number_of_games)+1):
# #     print(f'{league} - {book}: {z}/{int(number_of_games)}')
# #     matchup = scrape(z)
# #     if matchup:
# #         all_matchups.append(matchup)

# # print(f'Total matchups scraped: {len(all_matchups)}')

# # #Writes to JSON
# # try:
# #     with open('../../Data/ESPN/MLB.json', 'w', encoding='utf-8') as fp:
# #         json.dump(all_matchups, fp, indent=4)
# # except Exception as e:
# #     print(f"Error writing to file: {e}")

# # driver.quit()
