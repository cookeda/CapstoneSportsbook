import scrapy


class CbbSpider(scrapy.Spider):
    name = "CBB"
    allowed_domains = ["www.teamrankings.com"]
    base_url = "https://www.teamrankings.com/ncb/teams/?group=0"

    def start_requests(self):
        yield scrapy.Request(self.base_url, callback=self.parse)


    def parse(self, response):
        # Navigate to the table body
        links = response.xpath('/html/body/div[3]/div[1]/div[4]/main/div[2]/div/div/table/tbody/tr/td[1]/a/@href').extract()
        
        for link in links:
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_team, meta={'team_href': link})
                
    def parse_link_page(self, response):
        # This is where you process the page that each link leads to
        # For demonstration, let's just log the URL of the page we have followed
        yield {'url': response['team_href']}