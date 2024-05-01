import subprocess
import time
import os

print("Sorting Odds")


process1 = subprocess.Popen(["python", "./league_best_odds.py", "MLB"])
process2 = subprocess.Popen(["python", "./league_best_odds.py", "NBA"])

process3 = subprocess.Popen(["python", "./aggregate_odds.py", "NBA"])
process4 = subprocess.Popen(["python", "./aggregate_odds.py", "MLB"])

process1.wait()
process2.wait()
process3.wait()
process4.wait()

process5 = subprocess.Popen(["python", "combine.py"])
process5.wait()

process6 = subprocess.Popen(["python", "agg_combine.py"])
process6.wait()

# Edit I have no idea why I have the other matchups.json writer
#print(os.getcwd())
process7 = subprocess.Popen(["python", "matchups-writer.py", "Clean/Best Odds.json", "../../DegenBets/Data/script/matchups.json"])
process7.wait()

# process8 = subprocess.Popen(["python", "script.py"], cwd="../../Results")
# process8.wait()
print("Sorting complete.")
