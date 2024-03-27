cd OddsHistory
scrapy crawl NBA -o NBA.json
cd ../
cd Scrapers/Books
python book_scripts.py
cd ../../Data Collecting Src/
python MLBScrape.py
python NBAScrape.py
python CBBScrape.py
python Sort.py
python alg.py