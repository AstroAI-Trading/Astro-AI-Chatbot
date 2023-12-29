import scrapy
from selenium import webdriver
# Change this line in yahoo_finance.py
from yahoo_finance.spiders.ListOfCompanies import start_companies

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class YahooFinanceSpider(scrapy.Spider):
    name = 'yahoo_finance'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    start_urls = ['https://finance.yahoo.com/quote/{}/history?p={}']

    def start_requests(self):
        for company in start_companies:
            # Construct the URL for each company
            url = self.start_urls[0].format(company, company)

            # Yield the request with the company information
            yield scrapy.Request(url, callback=self.parse, meta={'company': company})

    def parse(self, response):
        # Extract the company from the meta information
        company = response.meta['company']

        # Print a sentence indicating the starting company
        self.log(f'Starting {company}')

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
                    'company': company,
                    'date': date,
                    'close_price': close_price,
                }

        driver.quit()

