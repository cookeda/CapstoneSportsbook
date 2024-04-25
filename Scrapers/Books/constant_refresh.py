import subprocess
import time

# Constant Refresh: Ment for updating odds during games.

process1 = subprocess.Popen(["python", "script.py"], cwd='DK')
process1.wait() 

process2 = subprocess.Popen(["python", "script.py"], cwd='ESPN') 
process3 = subprocess.Popen(["python", "script.py"], cwd='Bovada')
process2.wait() 
process3.wait()

process4 = subprocess.Popen(["python", "master_lite.py"])
print("Refresh done")