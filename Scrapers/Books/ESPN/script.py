import subprocess
import time

#process1 = subprocess.Popen(["python", "cbb_espn.py"]) # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python", "mlb_espn.py"])
process3 = subprocess.Popen(["python", "nba_espn.py"])

print("Scraping ESPN for: NBA, MLB")
#process1.wait()
process2.wait()
process3.wait()

# After scraping is complete, process the data with lite_writer.py
process5 = subprocess.Popen(["python", "../lite_writer.py", "../../Data/ESPN/NBA.json", "../../Data/ESPN/NBA_Lite.json"])
#process6 = subprocess.Popen(["python", "../lite_writer.py", "../../Data/ESPN/CBB.json", "../../Data/ESPN/CBB_Lite.json"])
process4 = subprocess.Popen(["python", "../lite_writer.py", "../../Data/ESPN/MLB.json", "../../Data/ESPN/MLB_Lite.json"])

print("ESPN Data processing complete.")