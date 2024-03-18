from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import os

# Setup Selenium WebDriver
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# Target link
link = "https://www.teamrankings.com/nfl/trends/win_trends/"

def scrape_teams(link, file):
    driver.get(link)
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')

    # Initialize list to hold team names
    teams = []

    # Iterate through each row in the table to extract team names
    for tr in soup.select('#DataTables_Table_0 tbody tr'):
        team_name = tr.select_one('td:nth-of-type(1) a').text.strip()
        teams.append(team_name)

    # Write team names to a JSON file
    with open(file, 'w') as fp:
        json.dump(teams, fp, indent=4)

    print(f"Extracted {len(teams)} team names into {file}")

def main():
    # Define output directory and file
    output_dir = "Dictionary/temp/"
    output_file = os.path.join(output_dir, "nfl_names.json")

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Scrape team names and write to file
    scrape_teams(link, output_file)

    # Close the WebDriver
    driver.close()

if __name__ == '__main__':
    main()
