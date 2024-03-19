import subprocess

process1 = subprocess.Popen(["python", "CBBScrape.py"]) # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python", "MLBScrape.py"])
process3 = subprocess.Popen(["python", "NBAScrape.py"])

print("Scraping Odds Trends for: NBA, CBB and MLB")

process1.wait() # Wait for process1 to finish (basically wait for script to finish)
process2.wait()
process3.wait()

#process4 = subprocess.Popen(["python", "Sort.py"])
#process5 = subprocess.Popen(["python", "alg.py"])