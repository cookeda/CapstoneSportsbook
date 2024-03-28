import scrapy
from bs4 import BeautifulSoup
from importlib import metadata
import re


class NbaSpider(scrapy.Spider):
    
    name = "NBA"
    allowed_domains = ["www.teamrankings.com"]
    base_url = "https://www.teamrankings.com/nba/"

    def start_requests(self):
        yield scrapy.Request(self.base_url, callback=self.parse)

    def parse(self, response):
        links = response.xpath('/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div/ul/li[7]/ul//a/@href').extract()
        for link in links:
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_table, meta = {'href': link})
    
    def parse_table(self, response):
 # Create a BeautifulSoup object
        #team = response.css('#h1-title').text()
        soup = BeautifulSoup(response.body, 'html.parser')
        
        # Locate the table by XPath or CSS Selector
        # Here we'll use the 'select' method with a CSS selector for simplicity
        # Adjust '.your-table-class' to match the actual class of your table or use other identifiers
        table = soup.select_one('html body div table tbody')
        
        if table:
            # Iterate over each row in the table
            for row in table.find_all('tr'):
                # Extract each cell (column) in the row
                columns = row.find_all('td')
                
                # Extract text from each cell
                # This creates a list of the cell texts
                data = [col.text.strip() for col in columns]
                date = data[0]
                team_href = response.meta['href']
                location = data[3]
                opponent = data[1]
                result = data[2]
                spread = str(data[6])
                match = re.search(r'\s(\d+)-(\d+)', result)
                team_name_part = team_href.split('/')[-2]
                # Split the team name part by hyphens and take the first part as the city name
                # This assumes the city name does not contain hyphens
                parts = team_name_part.split('-')
                if len(team_name_part.split('-')) == 2:
                    city_name = parts[0]
                else:
                    city_name = f'{parts[0]} {parts[1]}' if len(parts) > 1 else parts[0]
                ou_result = str(data[7])


                if location == 'Away':
                    
                    home_team = str(opponent).title()
                    home_score = match.group(1)
                    away_score = match.group(2)
                    away_team = str(city_name).title()
                    away_spread = spread if spread[0] == '-' else spread[1:] 
                    home_spread = away_spread[1:] if away_spread[0] == '-' else f'-{away_spread}'
                    total = ou_result[0]
                    

                else:
                    home_team = str(city_name).title()
                    away_team = str(opponent).title()
                    away_score = match.group(1)
                    home_score = match.group(2)
                    home_spread = spread if spread[0] == '-' else spread[1:] 
                    away_spread = home_spread[1:] if home_spread[0] == '-' else f'-{home_spread}'
                    total = ou_result[0]
                
                #Hard coded team city for the LA teams. 
                if home_team == "La Clippers": home_team = 'LA Clippers'
                if away_team == "La Clippers": away_team = 'LA Clippers'
                
                if home_team == "La Lakers": home_team = 'LA Lakers'
                if away_team == "La Lakers": away_team = 'LA Lakers'

                #Hard coded team city for the LA teams when the tem is the one seleceted. 
                if team_href == '/nba/team/los-angeles-clippers/' and location == 'Home': home_team = 'LA Clippers'
                if team_href == '/nba/team/los-angeles-clippers/' and location == 'Away': away_team = 'LA Clippers'
                if team_href == '/nba/team/los-angeles-lakers/' and location == 'Home': home_team = 'LA Lakers'
                if team_href == '/nba/team/los-angeles-lakers/' and location == 'Away': away_team = 'LA Lakers'
                if team_href == '/nba/team/los-angeles-lakers/' and home_team == 'Los Angeles' and location == 'Neutral': home_team = 'LA Lakers'

                # Assuming the first column is the team name and the rest are data points
                # Adjust the dictionary keys according to your table's structure
                if data:
                    date = data[0]
                    yield {
                        'Date': date,
                        'Home Team': home_team,
                        'Home Spread': home_spread,
                        'Home Score': home_score,
                        'Away Team': away_team,
                        'Away Spread': away_spread,
                        'Away Score': away_score,
                        'OU Result': total
                    }