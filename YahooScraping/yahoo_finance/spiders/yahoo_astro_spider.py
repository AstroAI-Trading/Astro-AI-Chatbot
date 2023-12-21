from typing import Iterable

import scrapy
from scrapy import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fred_scraping.fred_scraping.spiders.urls import yahoo_finance_urls


class YahooFinanceSpider(scrapy.Spider):
    name = 'yahoo_finance'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    start_urls = yahoo_finance_urls
    # start_urls = []
    scraped_data = []

    def __init__(self, *args, **kwargs):
        super(YahooFinanceSpider, self).__init__(*args, **kwargs)
        start_url = [kwargs.get('start_url')]
        scraped_data = [kwargs.get('scraped_data')]

        self.start_urls = [start_url] if start_url is not None else self.logger.warning(
            'start_url is None. The spider will not start.')

        self.scraped_data = scraped_data if scraped_data is not None else []

    def parse(self, response, **kwargs):
        # Use Selenium to load the page with dynamic content
        options = Options()
        options.headless = True  # Use this line to set headless mode

        # Specify the path to your Chrome driver executable if it's not in your PATH
        # driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=options)
        driver = webdriver.Chrome(options=options)
        driver.get(response.url)

        # Scroll to the bottom of the page to load all historical data
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(60)

        # Get the updated page content
        new_response = scrapy.Selector(text=driver.page_source)

        rows = new_response.css('tbody tr')
        for row in rows:
            date = row.css('td:nth-child(1) span::text').get()
            close_price = row.css('td:nth-child(6) span::text').get()

            if date and close_price:
                yield {
                    'date': date,
                    'close_price': close_price
                }

        driver.quit()

    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)
