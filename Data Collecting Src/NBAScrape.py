import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
webdriver.Chrome
from selenium.webdriver.chrome.options import Options
import json
import os

# Global Variables
options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
driver = webdriver.Chrome(options=options)
link = "https://www.teamrankings.com/nba/trends/"

# Gets every team's % for a given stat (type)
def scrape(link, file, type):
    driver.get(link)

    wait = WebDriverWait(driver, 10)
    first_team_xpath = "//*[@id='DataTables_Table_0']/tbody/tr[1]/td[1]/a"
    wait.until(EC.presence_of_element_located((By.XPATH, first_team_xpath)))

    cover = {}
    i = 1
    while i <= 30:
        team = driver.find_element(By.XPATH, "//*[@id='DataTables_Table_0']/tbody/tr[" + str(i) + "]/td[1]/a").text
        percent = driver.find_element(By.XPATH, "//*[@id='DataTables_Table_0']/tbody/tr[" + str(i) + "]/td[3]").text
        plusminus = driver.find_element(By.XPATH, "//*[@id='DataTables_Table_0']/tbody/tr[" + str(i) + "]/td[5]").text
        if plusminus == "0.0":
            plusminus = "+0.0"
        cover["Team"] = team
        cover[type + " %"] = percent
        i += 1
        with open(file, 'a') as fp:
            fp.write(json.dumps(cover) + " " + plusminus + '\n')
            print(str(i-1) + "/30")
    print("Done")

# Removes file if it already exists for a clean start
def cleanfile(file):
    try:
        os.remove(file)
    except FileNotFoundError:
        open(file, 'a')

# Calls all methods
# Removes files if they already exist
# Scrapes O/U and Cover for current season, Last 10 Years, and All Time
# Add implementation for other stuff (ex: home and away etc)
# Might have to break this into different classes due to weird runtime issues
def main():
    # Clean Files
    direct = "../data/NBA"
    cleanfile(direct + "/over/CurrentSeasonOU.jl")
    cleanfile(direct + "/cover/CurrentSeasonCover.jl")
    cleanfile(direct + "/cover/10YearCover.jl")
    cleanfile(direct + "/over/10YearOU.jl")
    cleanfile(direct + "/cover/AllTimeCover.jl")
    cleanfile(direct + "/over/AllTimeOU.jl")
    cleanfile(direct + "/cover/homeCover.jl")
    cleanfile(direct + "/over/homeOver.jl")
    cleanfile(direct + "/cover/awayCover.jl")
    cleanfile(direct + "/over/awayOver.jl")

    tasks = [
        {"message": "Starting This Year's Stats", "url": "ou_trends/?range=yearly_2023_2024",
         "file": "../data/NBA/over/CurrentSeasonOU.jl", "type": "Over"},
        {"message": "Starting This Year's Stats", "url": "ats_trends/?range=yearly_2023_2024",
         "file": "../data/NBA/cover/CurrentSeasonCover.jl", "type": "Cover"},
        {"message": "Starting Last 10 Years", "url": "ats_trends/?range=yearly_since_2013_2014",
         "file": "../data/NBA/cover/10YearCover.jl", "type": "Cover"},
        {"message": "Starting Last 10 Years", "url": "ou_trends/?range=yearly_since_2013_2014",
         "file": "../data/NBA/over/10YearOU.jl", "type": "Over"},
        {"message": "Starting All Time Stats", "url": "ats_trends/?range=yearly_all",
         "file": "../data/NBA/cover/AllTimeCover.jl", "type": "Cover"},
        {"message": "Starting All Time Stats", "url": "ou_trends/?range=yearly_all",
         "file": "../data/NBA/over/AllTimeOU.jl", "type": "Over"},
        {"message": "Starting Current Home Stats", "url": "ats_trends/?sc=is_home",
         "file": "../data/NBA/cover/homeCover.jl", "type": "Cover"},
        {"message": "Starting Current Home Stats", "url": "ou_trends/?sc=is_home",
         "file": "../data/NBA/over/homeOver.jl", "type": "Over"},
        {"message": "Starting Current Away Stats", "url": "ats_trends/?sc=is_away",
         "file": "../data/NBA/cover/awayCover.jl", "type": "Cover"},
        {"message": "Starting Current Away Stats", "url": "ou_trends/?sc=is_away",
         "file": "../data/NBA/over/awayOver.jl", "type": "Over"}
    ]

    for task in tasks:
            print(task["message"])
            scrape(link + task["url"], task["file"], task["type"])

    driver.close()

# Runs Program
if __name__ == '__main__':
    main()