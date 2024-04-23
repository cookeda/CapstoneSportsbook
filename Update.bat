@echo off
:: Capture start time
set start_time=%time%

:: Scrape Matchups
cd ./Scrapers/Books
python constant_refresh.py

:: Run Algorithms
cd ../../Data Collecting Src/
:: python alg.py > ../Results/alg_results.txt
python game.py > ../Results/game_results.txt

cd ../Results/
python summary.py
python merger.py

cd ../DegenBets
::npx eas update --auto 
cd ../

:: Capture end time
set end_time=%time%

cd ../

