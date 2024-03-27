from selenium import webdriver
webdriver.Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import json
import os

# Global Variables
options = Options()
options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
link = "https://www.teamrankings.com/nba/trends/"

# Gets every team's % for a given stat (type)
def scrape(link, file, type):
    driver.get(link)
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')

    cover = {}
    for i, tr in enumerate(soup.select('#DataTables_Table_0 tbody tr'), start=1):
        team = tr.select_one('td:nth-of-type(1) a').text.strip()
        percent = tr.select_one('td:nth-of-type(3)').text.strip()
        mov = tr.select_one('td:nth-of-type(4)').text.strip()
        if mov == "0.0":
            mov = "+0.0"
        cover["Team"] = team
        cover[type + " %"] = percent
        i += 1
        with open(file, 'a') as fp:
            fp.write(json.dumps(cover) + " " + mov + '\n')
        if i >= 31: break
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
    # Connor
    direct = "../data/NBA"
    # Devin
    #direct = "data/NBA"
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
         "file": direct + "/over/CurrentSeasonOU.jl", "type": "Over"},
        {"message": "Starting This Year's Stats", "url": "ats_trends/?range=yearly_2023_2024",
         "file": direct + "/cover/CurrentSeasonCover.jl", "type": "Cover"},
        {"message": "Starting Last 10 Years", "url": "ats_trends/?range=yearly_since_2013_2014",
         "file": direct + "/cover/10YearCover.jl", "type": "Cover"},
        {"message": "Starting Last 10 Years", "url": "ou_trends/?range=yearly_since_2013_2014",
         "file": direct + "/over/10YearOU.jl", "type": "Over"},
        {"message": "Starting All Time Stats", "url": "ats_trends/?range=yearly_all",
         "file": direct + "/cover/AllTimeCover.jl", "type": "Cover"},
        {"message": "Starting All Time Stats", "url": "ou_trends/?range=yearly_all",
         "file": direct + "/over/AllTimeOU.jl", "type": "Over"},
        {"message": "Starting Current Home Stats", "url": "ats_trends/?sc=is_home",
         "file": direct + "/cover/homeCover.jl", "type": "Cover"},
        {"message": "Starting Current Home Stats", "url": "ou_trends/?sc=is_home",
         "file": direct + "/over/homeOver.jl", "type": "Over"},
        {"message": "Starting Current Away Stats", "url": "ats_trends/?sc=is_away",
         "file": direct + "/cover/awayCover.jl", "type": "Cover"},
        {"message": "Starting Current Away Stats", "url": "ou_trends/?sc=is_away",
         "file": direct + "/over/awayOver.jl", "type": "Over"}
    ]

    for task in tasks:
            print(task["message"])
            scrape(link + task["url"], task["file"], task["type"])

    driver.close()

# Runs Program
if __name__ == '__main__':
    main()