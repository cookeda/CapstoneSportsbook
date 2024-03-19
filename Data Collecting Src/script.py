import subprocess

process1 = subprocess.Popen(["python", "Data Collecting Src\\CBBScrape.py"]) # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python", "Data Collecting Src\\MLBScrape.py"])
process3 = subprocess.Popen(["python", "Data Collecting Src\\NBAScrape.py"])
process4 = subprocess.Popen(["python", "Data Collecting Src\\Sort.py"])

process1.wait() # Wait for process1 to finish (basically wait for script to finish)
process2.wait()
process3.wait()