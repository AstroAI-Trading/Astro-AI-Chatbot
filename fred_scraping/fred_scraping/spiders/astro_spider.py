from typing import Any
import scrapy
from scrapy.http import Response
from fred_scraping.fred_scraping.items import FredScrapingItem

class AstroSpider(scrapy.Spider):
    name = 'Astro Spider'
    start_urls = ['https://fred.stlouisfed.org/', 'https://finance.yahoo.com/']


    def parse(self, response: Response, **kwargs: Any) -> Any:
        if str(response.status).startswith('2') and any(response._get_url().startswith(start_url) for start_url in self.start_urls):
            items = response.css('.item-selector')

            for item in items:
                fred_item = FredScrapingItem()
                
                fred_item['title'] = item.css('title::text').get()
                fred_item['description'] = item.css('p::text').get()
                fred_item['url'] = response.url

                fred_item['data'] = {
                    'title': fred_item['title'],
                    'description': fred_item['description'],
                    'url': fred_item['url']
                }

                if any(fred_item.values()):
                    self.logger.info(f'Successfully yielded {response.url}.')
                    yield fred_item
                else:
                    self.logger.warning(f"The url {response.url} doesn't have the required data.")
        else:
            self.logger.warning(f'Skipping non-valid url {response.url}.')