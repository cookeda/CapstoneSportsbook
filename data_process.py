import os
import subprocess
import datetime

# Generate summary and merge results
os.chdir('../Results/')
subprocess.run(['python', 'script.py'])

# Data Processing and Updates
os.chdir('../Scrapers/Data Processing')
subprocess.run(['python', 'script.py'])

