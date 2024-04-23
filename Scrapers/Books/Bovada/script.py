import subprocess
import time

#process1 = subprocess.Popen(["python", "cbb_espn.py"]) # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python", "mlb_bovada.py"])
process3 = subprocess.Popen(["python", "nba_bovada.py"])

print("Scraping Bovada for: NBA, MLB")
#process1.wait()
process2.wait()
process3.wait()
time.sleep(3)

process4 = subprocess.Popen(["python", "../lite_writer.py", "../../Data/Bovada/MLB.json", "../../Data/Bovada/MLB_Lite.json"])
process5 = subprocess.Popen(["python", "../lite_writer.py", "../../Data/Bovada/NBA.json", "../../Data/Bovada/NBA_Lite.json"])

process5.wait()
process4.wait()

print("Bovada Data processing complete.")