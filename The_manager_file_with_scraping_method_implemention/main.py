from scrapy.crawler import CrawlerProcess
from YahooScraping.yahoo_finance.spiders.yahoo_astro_spider import YahooFinanceSpider
from fred_scraping.fred_scraping.spiders.astro_spider import AstroSpider
from urllib.parse import urlparse




def scraping_specified_link(link):
    # Parse the URL to determine the domain
    domain = urlparse(link).hostname

    # Check if the domain is from Yahoo Finance or Fred
    if 'yahoo.com' in domain:
        spider = YahooFinanceSpider
    elif 'fred.stlouisfed.org' in domain:
        spider = AstroSpider
    else:
        print(f"Invalid URL: {link}")
        return

    # Run the Scrapy spider
    process = CrawlerProcess()
    process.crawl(spider, start_url=link)
    process.start()

    print(f"Scraping completed for URL: {link}")

if __name__ == '__main__':
    # Example usage:
    link_to_scrape = input("Please enter the url you want to scrape: ")
    scraping_specified_link(link_to_scrape)
# https://fred.stlouisfed.org/series/CORESTICKM159SFRBATL