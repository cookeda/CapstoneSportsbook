import os
import subprocess
import datetime
import time

# Capture start time
start_time = datetime.datetime.now()

# Scrape Matchups
os.chdir("./Scrapers/Books")
subprocess.run(['python', 'daily_refresh.py'])

# Run Algorithm
os.chdir('../../Data Collecting Src/')
subprocess.run(['python', 'game.py'], stdout=open('../Results/game_results.txt', 'w', encoding='utf-8'))

# Data Processing and Updates
os.chdir('../Scrapers/Data Processing')
subprocess.run(['python', 'script.py'])


# Generate summary and merge results
os.chdir('../../Results/')
subprocess.run(['python', 'script.py'])

os.chdir('../OddsHistory/History')
subprocess.run(['python', 'sorting_algorithm.py'], stdout=open('../../Results/xHitRate.txt', 'w', encoding='utf-8'))


# Uncomment the following line to enable the auto update command
# os.chdir('../../DegenBets')
# subprocess.run(['npx', 'eas', 'update', '--auto'])

# Capture end time
end_time = datetime.datetime.now()

# Return to the initial directory (adjust path as necessary)
os.chdir('../..')

# Print elapsed time
print(f"Script started at: {start_time}")
print(f"Script ended at: {end_time}")
print(f"Total execution time: {end_time - start_time}")
