import os
import subprocess
from datetime import datetime

def main():
    # Capture start time
    start_time = datetime.now()
    
    # Run History in Data Collecting Src
    os.chdir("/media/myfiles/CapstoneSportsbook/Data Collecting Src")
    subprocess.run(['python3.10', 'history.py'])

    # Scrape Adv League Data
    os.chdir("../OddsHistory")
    try:
        os.remove("NBA.json")
    except FileNotFoundError:
        pass
    try:
        os.remove("MLB.json")
    except FileNotFoundError:
        pass
    subprocess.run(['scrapy', 'crawl', 'NBA', '-o', 'NBA.json'])
    subprocess.run(['scrapy', 'crawl', 'MLB', '-o', 'MLB.json'])

    # Scrape League Data
    os.chdir("../Data Collecting Src")
    subprocess.run(['python3.10', 'MLBScrape.py'])
    subprocess.run(['python3.10', 'NBAScrape.py'])
    #subprocess.run(['python3.10', 'CBBScrape.py'])
    subprocess.run(['python3.10', 'Sort.py'])
    os.chdir("../")

    # Scrape Matchups
    os.chdir("./Scrapers/Books")
    subprocess.run(['python3.10', 'daily_refresh.py'])

    # Run Algorithms
    os.chdir("../../Data Collecting Src")
    with open("../Results/alg_results.txt", "w") as f:
        subprocess.run(['python3.10', 'alg.py'], stdout=f)
    with open("../Results/game_results.txt", "w") as f:
        subprocess.run(['python3.10', 'game.py'], stdout=f)
    with open("../Results/SuccessData_results.txt", "w") as f:
        subprocess.run(['python3.10', 'SuccessData.py'], stdout=f)
    os.chdir("../Results")
    subprocess.run(['python3.10', 'summary.py'])

    # Capture end time
    end_time = datetime.now()

    # Display start and end times
    print("Start Time:", start_time)
    print("End Time:", end_time)

if __name__ == "__main__":
    main()
