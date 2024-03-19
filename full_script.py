import subprocess
import time

directory_path = 'dk'

process1 = subprocess.Popen(["python", "book_scripts.py"], cwd='Scrapers/Books') # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python", "script.py"], cwd='Data Collecting Src')


process1.wait() 
process2.wait()
print("Ran script files for Odds trends and book files")

#time.sleep(5)

#process4 = subprocess.Popen(["python", "Sort.py"], cwd='Data_Collecting_Src')
#process5 = subprocess.Popen(["python", "alg.py"], cwd='Data_Collecting_Src')