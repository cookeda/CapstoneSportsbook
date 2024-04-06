import subprocess
import time

process1 = subprocess.Popen(["python", "cbb_dk.py"]) # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python", "mlb_dk.py"])
process3 = subprocess.Popen(["python", "nba_dk.py"])

print("Scraping DraftKings for: CBB, NBA, MLB")
process1.wait()
process2.wait()
process3.wait()


# After scraping is complete, process the data with lite_writer.py
process5 = subprocess.Popen(["python", "../lite_writer.py", "../../Data/DK/NBA.json", "../../Data/DK/NBA_Lite.json"])
process6 = subprocess.Popen(["python", "../lite_writer.py", "../../Data/DK/CBB.json", "../../Data/DK/CBB_Lite.json"])
process4 = subprocess.Popen(["python", "../lite_writer.py", "../../Data/DK/MLB.json", "../../Data/DK/MLB_Lite.json"])

print("DK Data processing complete.")
