import subprocess
import time

process1 = subprocess.Popen(["python", "script.py"], cwd='DK') # Create and launch process pop.py using python interpreter
process1.wait()
print("DK data scraped for the first time today")


process2 = subprocess.Popen(["python", "script.py"], cwd='ESPN') # Create and launch
process3 = subprocess.Popen(["python", "script.py"], cwd='Bovada')

process2.wait()
process3.wait()

print("All book data scraped")
#time.sleep(5)

#process4 = subprocess.Popen(["python", "Sort.py"])
#process5 = subprocess.Popen(["python", "alg.py"])