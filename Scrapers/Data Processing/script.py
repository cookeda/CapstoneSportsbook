import subprocess
import time

print("Sorting Odds")

process1 = subprocess.Popen(["python", "./league_best_odds.py", "nba"])
process2 = subprocess.Popen(["python", "./league_best_odds.py", "mlb"])
process3 = subprocess.Popen(["python", "./aggregate_odds.py", "nba"])
process4 = subprocess.Popen(["python", "./aggregate_odds.py", "mlb"])

process1.wait()
process2.wait()
process3.wait()
process4.wait()

process5 = subprocess.Popen(["python", "combine.py"])
process5.wait()


print("Sorting complete.")