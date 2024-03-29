@echo off
:: Capture start time
set start_time=%time%

:: Scrape Adv League Data
cd OddsHistory
scrapy crawl NBA -o NBA.json
#scrapy crawl MLB -o MLB.json
:: Scrape Matchups
cd ../
cd Scrapers/Books
python book_scripts.py

:: Scrape League Data
cd ../../Data Collecting Src/
python MLBScrape.py
python NBAScrape.py
python CBBScrape.py
python Sort.py
python alg.py
cd ../

:: Capture end time
set end_time=%time%

:: Display start and end times
echo Start Time: %start_time%
echo End Time: %end_time%