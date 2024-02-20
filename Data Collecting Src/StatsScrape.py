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
        cover["Team"] = team
        cover[type + " %"] = percent
        i += 1
        with open(file, 'a') as fp:
            fp.write(json.dumps(cover) + '\n')
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
    cleanfile("../data/cover/CurrentSeasonCover.jl")
    cleanfile("../data/over/CurrentSeasonOU.jl")
    cleanfile("../data/cover/10YearCover.jl")
    cleanfile("../data/over/10YearOU.jl")
    cleanfile("../data/cover/AllTimeCover.jl")
    cleanfile("../data/over/AllTimeOU.jl")
    cleanfile("../data/cover/home/homeCover.jl")
    cleanfile("../data/over/home/homeOver.jl")
    cleanfile("../data/cover/away/awayCover.jl")
    cleanfile("../data/over/away/awayOver.jl")

    # This Year's Cover and O/U
    print("Starting This Year's Stats")
    scrape(link + "ou_trends/?range=yearly_2023_2024", "../data/over/CurrentSeasonOU.jl", "Over")
    scrape(link + "ats_trends/?range=yearly_2023_2024", "../data/cover/CurrentSeasonCover.jl", "Cover")


    # Last 10 Years Cover and O/U
    print("Starting Last 10 Years")
    scrape(link + "ats_trends/?range=yearly_since_2013_2014", "../data/cover/10YearCover.jl", "Cover")
    scrape(link + "ou_trends/?range=yearly_since_2013_2014", "../data/over/10YearOU.jl", "Over")

    # All Time Cover and O/U
    print("Starting All Time Stats")
    scrape(link + "ats_trends/?range=yearly_all", "../data/cover/AllTimeCover.jl", "Cover")
    scrape(link + "ou_trends/?range=yearly_all", "../data/over/AllTimeOU.jl", "Over")

    # Current season home Cover and OU
    print("Starting Current Home Stats")
    scrape(link + "ats_trends/?sc=is_home", "../data/cover/homeCover.jl", "Cover")
    scrape(link + "/ou_trends/?sc=is_home", "../data/over/homeOver.jl", "Over")

    # Current season Away Cover and OU
    print("Starting Current Away Stats")
    scrape(link + "ats_trends/?sc=is_away", "../data/cover/awayCover.jl", "Cover")
    scrape(link + "/ou_trends/?sc=is_away", "../data/over/awayOver.jl", "Over")


    # End
    driver.close()

# Runs Program
if __name__ == '__main__':
    main()