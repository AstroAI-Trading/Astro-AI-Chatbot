# import subprocess
#
# def run_spider(tickers, start_date, end_date):
#     tickers_str = ",".join(tickers)
#     command = f"scrapy crawl yahoo_finance -a tickers={tickers_str} -a start_date={start_date} -a end_date={end_date} -o output.csv"
#     subprocess.run(command, shell=True)
#
# def main():
#     # Get user input for start and end dates
#     start_date = input("Enter start date (YYYY-MM-DD): ")
#     end_date = input("Enter end date (YYYY-MM-DD): ")
#
#     # Get user input for the list of primary company tickers
#     tickers_input = input("Enter primary company tickers separated by commas (e.g., AAPL,GOOGL): ")
#     tickers = [ticker.strip() for ticker in tickers_input.split(',')]
#
#     # Run the spider with user inputs
#     run_spider(tickers, start_date, end_date)
#
# if __name__ == "__main__":
#     main()

import subprocess
import pandas as pd
import json
from tabulate import tabulate
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from yahoo_finance.yahoo_finance.spiders.yahoo_finance import YahooFinanceSpider


def get_competitors(primary_ticker):
    competitors_data = pd.read_csv("yahoo_finance/yahoo_finance/spiders/Comepititors.json", index_col=0, header=None, names=["competitors"])
    competitors_str = competitors_data["competitors"].get(primary_ticker, '')
    competitors = [c.strip() for c in competitors_str.split(',')]
    return competitors

def run_spider(primary_ticker, start_date, end_date, competitors):
    tickers = [primary_ticker] + competitors
    tickers_str = ",".join(tickers)

    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json',
        'LOG_LEVEL': 'INFO',  # Adjust log level as needed
    })

    process.crawl(YahooFinanceSpider, tickers=tickers_str, start_date=start_date, end_date=end_date)
    process.start()

def main():
    primary_ticker = input("Enter primary company ticker (e.g., AACG): ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    competitors = get_competitors(primary_ticker)

    if not competitors:
        print(f"No competitors found for {primary_ticker}. Exiting.")
        return

    run_spider(primary_ticker, start_date, end_date, competitors)

    try:
        df = pd.read_json('output.json')
        df = df.transpose()
        df.columns = df.columns.astype(str)

        csv_filename = 'output_table.csv'
        df.to_csv(csv_filename, index=False)

        print("\nFormatted Output:")
        print(tabulate(df, headers='keys', tablefmt='grid'))
        print(f"\nData saved to {csv_filename}")

    except ValueError as e:
        print(f"Error: {e}")
        with open('output.json', 'r') as json_file:
            content = json_file.read()
            print(f"JSON Content: {content}")

if __name__ == "__main__":
    main()


