import os
import subprocess
import datetime

# Capture start time
start_time = datetime.datetime.now()

# Scrape Matchups
os.chdir('./Scrapers/Books')
subprocess.run(['python', 'constant_refresh.py'])

# Run Algorithms
os.chdir('../../Data Collecting Src/')
# Uncomment the following line to execute alg.py and redirect output to a text file
# subprocess.run(['python', 'alg.py'], stdout=open('../Results/alg_results.txt', 'w'))
subprocess.run(['python', 'game.py'], stdout=open('../Results/game_results.txt', 'w'))

# Generate summary and merge results
os.chdir('../Results/')
subprocess.run(['python', 'summary.py'])
subprocess.run(['python', 'merger.py'])
# Uncomment to enable sorting matchup page (Live games not implemeneted yet)
# Data Processing and Updates
# os.chdir('../Scrapers/Data Processing')
# subprocess.run(['python', 'script.py'])
# os.chdir('../../DegenBets')
# Uncomment the following line to enable the auto update command
# subprocess.run(['npx', 'eas', 'update', '--auto'])

# Capture end time
end_time = datetime.datetime.now()

# Return to the initial directory (adjust path as necessary)
os.chdir('../..')

# Print elapsed time
print(f"Script started at: {start_time}")
print(f"Script ended at: {end_time}")
print(f"Total execution time: {end_time - start_time}")
