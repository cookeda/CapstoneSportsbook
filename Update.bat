@echo off
:: Capture start time
set start_time=%time%

:: Scrape Matchups
cd ./Scrapers/Books
python book_scripts.py
cd ./DK
python dk_lite_writer.py ../../Data/DK/MLB.json ../../Data/DK/MLB_Lite.json
python dk_lite_writer.py ../../Data/DK/NBA.json ../../Data/DK/NBA_Lite.json
python dk_lite_writer.py ../../Data/DK/CBB.json ../../Data/DK/CBB_Lite.json
cd ../

:: Run Algorithms
cd ../../Data Collecting Src/

python alg.py > ../Results/alg_results.txt
python game.py > ../Results/game_results.txt

:: Capture end time
set end_time=%time%

:: Display start and end times
echo Start Time: %start_time%
echo End Time: %end_time%