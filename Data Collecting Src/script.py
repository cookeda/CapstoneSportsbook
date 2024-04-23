import subprocess
import time

process1 = subprocess.Popen(["python", "MLBScrape.py"])
process2 = subprocess.Popen(["python", "NBAScrape.py"])

process1.wait()
process2.wait()
time.sleep(3)

process3 = subprocess.Popen(["python", "Sort.py"])
process3.wait()