# import scrapy
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# from selenium.webdriver.common.keys import Keys
#
#
# # Change this line in yahoo_finance.py
# from yahoo_finance.spiders.ListOfCompanies import start_companies
#
# class YahooFinanceSpider(scrapy.Spider):
#     name = 'yahoo_finance'
#     custom_settings = {
#         'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     }
#
#     start_urls = ['https://finance.yahoo.com/quote/{}/history?p={}']
#
#     def start_requests(self):
#         for company in start_companies:
#             # Construct the URL for each company
#             url = self.start_urls[0].format(company, company)
#
#             # Yield the request with the company information
#             yield scrapy.Request(url, callback=self.parse, meta={'company': company})
#
#     def parse(self, response):
#         company = response.meta['company']
#         self.log(f'Starting {company}')
#
#         options = Options()
#         options.headless = True
#         driver = webdriver.Chrome(options=options)
#         driver.get(response.url)
#
#         # Wait for the historical data table to be present
#         WebDriverWait(driver, 15).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody tr'))
#         )
#
#         # Scroll to the bottom of the page
#         body = driver.find_element(By.TAG_NAME, 'body')
#         body.send_keys(Keys.END)
#
#         # Add a delay to allow the page to load
#         time.sleep(15)
#
#         # Get the updated page content
#         new_response = scrapy.Selector(text=driver.page_source)
#
#         rows = new_response.css('tbody tr')
#         for row in rows:
#             date = row.css('td:nth-child(1) span::text').get()
#             close_price = row.css('td:nth-child(6) span::text').get()
#
#             if date and close_price:
#                 yield {
#                     'company': company,
#                     'date': date,
#                     'close_price': close_price,
#                 }
#
#         driver.quit()



# scrapy crawl yahoo_finance -O test.json
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import  time

class YahooFinanceSpider(scrapy.Spider):
    name = 'yahoo_finance'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'FEEDS': {
            'output.json': {
                'format': 'json',
                'overwrite': True,  # Set this to True to overwrite the file each time
            },
        },
    }

    def __init__(self, tickers='', start_date='', end_date='', *args, **kwargs):
        super(YahooFinanceSpider, self).__init__(*args, **kwargs)
        self.tickers = tickers.split(',')
        self.start_date = start_date
        self.end_date = end_date

    def start_requests(self):
        for ticker in self.tickers:
            url = f'https://finance.yahoo.com/quote/{ticker}/history?p={ticker}'
            yield scrapy.Request(url, callback=self.parse, meta={'ticker': ticker})

    def parse(self, response, **kwargs):
        ticker = response.meta['ticker']
        self.log(f'Starting {ticker}')

        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(response.url)

        # Wait for the historical data table to be present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody tr'))
        )

        # Scroll to the bottom of the page
        body = driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.END)

        # Add a delay to allow the page to load
        time.sleep(15)

        # Get the updated page content
        new_response = scrapy.Selector(text=driver.page_source)

        rows = new_response.css('tbody tr')
        for row in rows:
            date = row.css('td:nth-child(1) span::text').get()
            close_price = row.css('td:nth-child(6) span::text').get()

            if date and close_price:
                yield {
                    'company': ticker,
                    'date': date,
                    'close_price': close_price,
                }

        driver.quit()




