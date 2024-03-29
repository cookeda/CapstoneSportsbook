import subprocess

def main():
    # Running scraping scripts
    print("Scraping DraftKings for: CBB, NBA, MLB")
    process1 = subprocess.Popen(["python", "cbb_dk.py"])  # CBB scraping script
    process2 = subprocess.Popen(["python", "mlb_dk.py"])  # MLB scraping script
    process3 = subprocess.Popen(["python", "nba_dk.py"])  # NBA scraping script
    
    # Wait for all scraping processes to complete
    process1.wait()
    process2.wait()
    process3.wait()

    # After scraping is done, start reformatting JSON files
    print("Reformatting JSON files...")
    subprocess.run(["python", "master_dk_lite.py", "../../Data/DK/CBB.json", "../../Data/DK/CBB_Lite.json"], check=True)
    subprocess.run(["python", "master_dk_lite.py", "../../Data/DK/NBA.json", "../../Data/DK/NBA_Lite.json"], check=True)
    subprocess.run(["python", "master_dk_lite.py", "../../Data/DK/MLB.json", "../../Data/DK/MLB_Lite.json"], check=True)
    
    # Further processing if needed
    # subprocess.run(["python", "Sort.py"])
    # subprocess.run(["python", "alg.py"])

if __name__ == "__main__":
    main()
