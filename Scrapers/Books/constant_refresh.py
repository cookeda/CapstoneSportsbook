import subprocess
import time

process1 = subprocess.Popen(["python", "script.py"], cwd='DK') # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python", "script.py"], cwd='ESPN') # Create and launch
process3 = subprocess.Popen(["python", "script.py"], cwd = 'Bovada')

process1.wait() # Wait for process1 to finish (basically wait for script to finish)
process2.wait() # Wait for process2 to finish (basically wait for script to finish)
process3.wait()

process3 = subprocess.Popen(["python", "master_lite.py"])

print("Refresh done")