@echo off
:: Capture start time
set start_time=%time%

:: Scrape Matchups
cd ./Scrapers/Books
python book_scripts.py

:: Run Algorithms
cd ../../Data Collecting Src/
python alg.py
python game.py > game_results.txt

:: Capture end time
set end_time=%time%

:: Display start and end times
echo Start Time: %start_time%
echo End Time: %end_time%