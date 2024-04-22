import hashlib
import json
import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc

league = 'MLB'
book = 'Bovada'


def find_element_text_or_default(driver, xpath, default='N/A', wait_time=10):
    """Finds text of a web element by xpath, returns default if not found within wait time."""
    try:
        element = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return element.text
    except Exception:
        return default
    
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

def scrape(matchup_num):
    """
    Scrapes betting information for a specific matchup from a webpage.

    This function navigates to specific elements on a webpage using XPath to extract information about a sports matchup. It retrieves details such as team names, spread values, moneyline (ML) values, total points, and start times. It then uses helper functions to find additional information like team rankings and IDs based on the scraped team names. Finally, it compiles all the information into a structured dictionary.

    Parameters:
    - matchup_num (int): The number of the matchup on the webpage, used to construct the XPath for locating elements.

    Returns:
    - list: A list containing a single dictionary with detailed betting and matchup information, including team names, IDs, rankings, and betting odds.
    """
    # Scraping various pieces of information using XPath. Each piece corresponds to a specific betting or game detail.
    away_team_text = find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/header/sp-competitor-coupon/a/div[1]/h4[1]/span[1]')
    home_team_text = find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/header/sp-competitor-coupon/a/div[1]/h4[2]/span[1]')
    away_spread_text = find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[1]/ul/li[1]/sp-outcome/button/sp-spread-outcome/span')
    away_spread_odds_text = find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[1]/ul/li[1]/sp-outcome/button/span[1]')
    total_text = find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[3]/ul/li[1]/sp-outcome/button/sp-total-outcome/span[2]')
    over_total_odds_text = find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[3]/ul/li[1]/sp-outcome/button/span[1]')
    away_ml_text = find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[2]/ul/li[1]/sp-outcome/button/span[1]')
    home_spread_text = find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[1]/ul/li[2]/sp-outcome/button/sp-spread-outcome/span')
    home_spread_odds_text = find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[1]/ul/li[2]/sp-outcome/button/span[1]')
    under_total_odds_text = find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[3]/ul/li[2]/sp-outcome/button/span[1]')
    home_ml_text = find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-outcomes/sp-two-way-vertical[2]/ul/li[2]/sp-outcome/button/span[1]')
    start_time_text = find_element_text_or_default(driver, f'/html/body/bx-site/ng-component/div[1]/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon[{matchup_num}]/sp-multi-markets/section/section/sp-score-coupon/span/time')
    
    # # Using helper functions to find team rankings and IDs based on the scraped team names.
    # away_team_rank_name = find_team_rank_name(away_team_text)  # Name from team rankings.com
    # home_team_rank_name = find_team_rank_name(home_team_text)  # Name from team rankings.com
    # away_team_id = find_team_id(away_team_text)  # Team
    # home_team_id = find_team_id(home_team_text)  # Team
    
    # # Generating unique identifiers for the matchup and the betting table.
    # matchup_id = encode_matchup_id(away_team_id, home_team_id, league)
    # bet_table_id = encode_bet_table_id(matchup_id, book)
    
    # Compiling all the scraped and generated information into a structured dictionary.
    info = [ 
        {
            #'BetTableId': bet_table_id,
            'Odds Table': {
                'Book Name': book,
                'Away Spread': away_spread_text, 
                'Away Spread Odds': away_spread_odds_text,
                'Away ML': away_ml_text,
                'Home Spread': home_spread_text, 
                'Home Spread Odds': home_spread_odds_text,
                'Home ML': home_ml_text,
                'Total': total_text[3:], 
                'Over Total Odds': over_total_odds_text, 
                'Under Total Odds': under_total_odds_text,
            },
            #'MatchupID': matchup_id,
            'Info Table': {                
                    'Away Team': away_team_text, 
             #       'Away Team Rank Name': away_team_rank_name, 
             #       'Away ID': away_team_id,
                    'Home Team': home_team_text, 
             #       'Home Team Rank Name': home_team_rank_name,
             #       'Home ID': home_team_id, 
                    'Start Time': start_time_text, 
                    'League': league
                }
            }
    ]
    
    # Printing the teams involved in the matchup for logging purposes.
    print(f'{away_team_text}, {home_team_text}')
    return info

def hash_teams(away_team, home_team):
    """Creates an MD5 hash for a game based on the team names."""
    hash_input = away_team + home_team
    return hashlib.md5(hash_input.encode()).hexdigest()

# Initialize the Chrome driver with undetected_chromedriver to avoid detection
options = uc.ChromeOptions()
options.headless = True
options.add_argument('--no-sandbox')
driver = uc.Chrome(options=options)

driver.get("https://www.bovada.lv/sports/baseball/mlb")
time.sleep(3)  # Allow some time for the page to load JavaScript content

# Replace 'your_xpath' with the actual XPaths for the elements
matchup_xpath = '//div[contains(@class,"Matchup")]'
print(scrape(1))
print(scrape(2))
driver.quit()