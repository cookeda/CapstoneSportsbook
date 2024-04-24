import subprocess
import time
import os

print("Sorting Odds")

print("NBA")
process1 = subprocess.Popen(["python", "./league_best_odds2.py", "nba"])
print("MLB")
process2 = subprocess.Popen(["python", "./league_best_odds.py", "mlb"])
process3 = subprocess.Popen(["python", "./aggregate_odds.py", "nba"])
process4 = subprocess.Popen(["python", "./aggregate_odds.py", "mlb"])

process1.wait()
process2.wait()
process3.wait()
process4.wait()

process5 = subprocess.Popen(["python", "combine.py"])
process5.wait()

print(os.getcwd())
process6 = subprocess.Popen(["python", "matchups-writer.py", "Clean\Best Odds.json", "../../DegenBets/Data/script/matchups.json"])
process6.wait()

process7 = subprocess.Popen(["python", "script.py"], cwd="../../Results")
process7.wait()
print("Sorting complete.")