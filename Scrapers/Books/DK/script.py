import subprocess
import time

process1 = subprocess.Popen(["python", "cbb_dk.py"]) # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python", "mlb_dk.py"])
process3 = subprocess.Popen(["python", "nba_dk.py"])

print("Scraping DraftKings for: CBB, NBA, MLB")

process1.wait() # Wait for process1 to finish (basically wait for script to finish)
process2.wait()
process3.wait()

process4 = subprocess.Popen(["python", "master_dk_lite.py"])

#time.sleep(5)

#process4 = subprocess.Popen(["python", "Sort.py"])
#process5 = subprocess.Popen(["python", "alg.py"])