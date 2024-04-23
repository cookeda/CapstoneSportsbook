import os
import subprocess
import datetime

# Capture start time
start_time = datetime.datetime.now()

# Scrape Matchups
os.chdir('/media/myfiles/CapstoneSportsbook/Scrapers/Books')
subprocess.run(['python', 'constant_refresh.py'])

# Run Algorithms
os.chdir('../../Data Collecting Src/')
# Uncomment the following line to enable execution of alg.py and output results to a text file
# subprocess.run(['python', 'alg.py'], stdout=open('../Results/alg_results.txt', 'w'))
subprocess.run(['python', 'game.py'], stdout=open('../Results/game_results.txt', 'w'))

# Generate summary and merge results
os.chdir('../Results/')
subprocess.run(['python', 'summary.py'])
subprocess.run(['python', 'merger.py'])

# Change to DegenBets directory and update if necessary
os.chdir('../DegenBets')
# Uncomment the following line to enable the auto update command
# subprocess.run(['npx', 'eas', 'update', '--auto'])

# Capture end time
end_time = datetime.datetime.now()

# Change back to the initial directory
os.chdir('../../..')

# Print elapsed time
print(f"Script started at: {start_time}")
print(f"Script ended at: {end_time}")
print(f"Total execution time: {end_time - start_time}")