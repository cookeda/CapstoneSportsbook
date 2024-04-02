@echo off
:: Capture start time
set start_time=%time%

:: Scrape Adv League Data
cd Scrapers/Books/
python book_scripts.py

:: Capture end time
set end_time=%time%

:: Display start and end times
echo Start Time: %start_time%
echo End Time: %end_time%