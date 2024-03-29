from selenium import webdriver
import requests
webdriver.Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


import json
import os

# Global Variables
options = Options()
options.add_argument('--headless')
options.add_argument('log-level=3')

# Initialize the Service
service = Service(ChromeDriverManager().install())

# Initialize WebDriver without the 'desired_capabilities' argument
driver = webdriver.Chrome(service=service, options=options)

link = "https://www.teamrankings.com/ncb/"

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
        if i >= 363: break
    print("Done")

def scrapePPG(link, file):
    # options = Options()
    # options.add_argument('--headless')
    # options.add_argument('log-level=3')

    # # Initialize the Service
    # service = Service(ChromeDriverManager().install())

    # # Initialize WebDriver without the 'desired_capabilities' argument
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome()
    driver.get(link)
    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')

    results = []  # Use a list to collect dictionaries
    for tr in soup.select('#DataTables_Table_0 tbody tr')[:363]:
        data_dict = {
            "Team": tr.select_one('td:nth-of-type(2)').text.strip(),
            "PPG": tr.select_one('td:nth-of-type(3)').text.strip(),
            "Last 3": tr.select_one('td:nth-of-type(4)').text.strip(),
            "Home": tr.select_one('td:nth-of-type(6)').text.strip(),
            "Away": tr.select_one('td:nth-of-type(7)').text.strip(),
        }
        results.append(data_dict)

    with open(file, 'a') as fp:
        for result in results:
            fp.write(json.dumps(result) + '\n')

    print("Done")
    driver.close()  # Close the browser window

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
    direct = "../data/CBB"
    # Devin
    #direct = "data/CBB"
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
    # NEW
    cleanfile(direct + "/over/PointAverages.jl")

    tasks = [
        {"message": "Starting This Year's Stats", "url": "trends/ou_trends/?range=yearly_2023_2024",
         "file": direct + "/over/CurrentSeasonOU.jl", "type": "Over"},
        {"message": "Starting This Year's Stats", "url": "trends/ats_trends/?range=yearly_2023_2024",
         "file": direct + "/cover/CurrentSeasonCover.jl", "type": "Cover"},
        {"message": "Starting Last 10 Years", "url": "trends/ats_trends/?range=yearly_since_2013_2014",
         "file": direct + "/cover/10YearCover.jl", "type": "Cover"},
        {"message": "Starting Last 10 Years", "url": "trends/ou_trends/?range=yearly_since_2013_2014",
         "file": direct + "/over/10YearOU.jl", "type": "Over"},
        {"message": "Starting All Time Stats", "url": "trends/ats_trends/?range=yearly_all",
         "file": direct + "/cover/AllTimeCover.jl", "type": "Cover"},
        {"message": "Starting All Time Stats", "url": "trends/ou_trends/?range=yearly_all",
         "file": direct + "/over/AllTimeOU.jl", "type": "Over"},
        {"message": "Starting Current Home Stats", "url": "trends/ats_trends/?sc=is_home",
         "file": direct + "/cover/homeCover.jl", "type": "Cover"},
        {"message": "Starting Current Home Stats", "url": "trends/ou_trends/?sc=is_home",
         "file": direct + "/over/homeOver.jl", "type": "Over"},
        {"message": "Starting Current Away Stats", "url": "trends/ats_trends/?sc=is_away",
         "file": direct + "/cover/awayCover.jl", "type": "Cover"},
        {"message": "Starting Current Away Stats", "url": "trends/ou_trends/?sc=is_away",
         "file": direct + "/over/awayOver.jl", "type": "Over"},
        {"message": "Starting Point Averages", "url": "stat/points-per-game",
         "file": direct + "/over/PointAverages.jl", "type": "Over"}
    ]

    for task in tasks:
        print(task["message"])
        if task['message'] == "Starting Point Averages":
            scrapePPG("https://www.teamrankings.com/ncaa-basketball/" + task["url"], task["file"])
        else:
            scrape(link + task["url"], task["file"], task["type"])

    driver.close()


# Runs Program
if __name__ == '__main__':
    main()