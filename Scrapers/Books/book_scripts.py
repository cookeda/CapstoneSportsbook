import subprocess
import time

directory_path = 'dk'

process1 = subprocess.Popen(["python", "script.py"], cwd=directory_path) # Create and launch process pop.py using python interpreter


process1.wait() 

#time.sleep(5)

#process4 = subprocess.Popen(["python", "Sort.py"])
#process5 = subprocess.Popen(["python", "alg.py"])