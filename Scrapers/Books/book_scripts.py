import subprocess
import time

process1 = subprocess.Popen(["python", "script.py"], cwd='DK') # Create and launch process pop.py using python interpreter
#process2 = subprocess.Popen(["python", "script.py"], cwd='ESPN') # Create and launch

process1.wait()
#process2.wait() 

#time.sleep(5)

#process4 = subprocess.Popen(["python", "Sort.py"])
#process5 = subprocess.Popen(["python", "alg.py"])