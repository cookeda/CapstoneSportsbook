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

def find_element_text_or_default(driver, xpath, default='N/A', wait_time=10):
    """Finds text of a web element by xpath, returns default if not found within wait time."""
    try:
        element = WebDriverWait(driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return element
    except Exception:
        return default

def hash_teams(away_team, home_team):
    """Creates an MD5 hash for a game based on the team names."""
    hash_input = away_team + home_team
    return hashlib.md5(hash_input.encode()).hexdigest()

# Initialize the Chrome driver with undetected_chromedriver to avoid detection
options = uc.ChromeOptions()
options.headless = True
options.add_argument('--no-sandbox')
driver = uc.Chrome(options=options)

driver.get("https://sportsbook.caesars.com/us/wa-ms/bet?dl=retail_mode")
time.sleep(5)  # Allow some time for the page to load JavaScript content

# Replace 'your_xpath' with the actual XPaths for the elements
matchup_xpath = '//div[contains(@class,"Matchup")]'
print(find_element_text_or_default(driver, "/html/body/div[2]/div/div[11]/div/div[1]/div/div[2]/div/div/div[4]/div/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div/div/a[1]/div/div/div[2]/div/span"))
