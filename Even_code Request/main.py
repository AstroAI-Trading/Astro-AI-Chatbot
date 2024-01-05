# Import necessary libraries and modules
import pandas as pd
import json
from tabulate import tabulate
from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from yahoo_finance.yahoo_finance.spiders.yahoo_finance import YahooFinanceSpider

# Function to get competitors for a primary ticker
def get_competitors(primary_ticker):
    # Read the CSV-like data into a DataFrame
    competitors_data = pd.read_csv("/Users/ajmalamir/Documents/New_yahoo_finance/Even_code Request/yahoo_finance/yahoo_finance/spiders/comeptitors_new.csv")

    # Find the row corresponding to the primary_ticker
    row = competitors_data[competitors_data['company'] == primary_ticker]

    # If the primary_ticker is found, extract competitors
    if not row.empty:
        competitors_str = row['competitors'].values[0]
        competitors = [c.strip() for c in competitors_str.split(',')]
        return competitors
    else:
        return []

# Function to run the Yahoo Finance spider
def run_spider(primary_ticker, start_date, end_date, competitors):
    # Create a list of tickers including the primary and its competitors
    tickers = [primary_ticker] + competitors
    tickers_str = ",".join(tickers)

    # Create a CrawlerProcess instance with settings
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json',
        'FEED_OVERWRITE': True,  # Set this to True to overwrite the file each time
        'LOG_LEVEL': 'INFO',  # Adjust log level as needed
    })

    # Run the YahooFinanceSpider with provided parameters
    process.crawl(YahooFinanceSpider, tickers=tickers_str, start_date=start_date, end_date=end_date)
    process.start()
# Function to save the report to an Excel sheet
def save_report_to_excel(df, file_path):
    # Save the DataFrame to an Excel file
    df.to_excel(file_path, index=False)

# Main function
def main():
    # Get user-provided primary company and start/end dates
    primary_ticker = input("Enter primary company ticker (e.g., AACG): ").upper()
    start_date = input("Enter start date (e.g., Jan 01, 2023): ").title()
    end_date = input("Enter end date (e.g., Jan 31, 2023): ").title()

    # Get competitors for the primary ticker
    competitors = get_competitors(primary_ticker)

    # If no competitors found, exit the program
    if not competitors:
        print(f"No competitors found for {primary_ticker}. Exiting.")
        return

    # Run the Yahoo Finance spider
    run_spider(primary_ticker, start_date, end_date, competitors)

    # Read competitors data from Competitors.csv
    competitors_df = pd.read_csv(
        '/Users/ajmalamir/Documents/New_yahoo_finance/Even_code Request/yahoo_finance/yahoo_finance/spiders/comeptitors_new.csv')

    # Get user-provided primary company and start/end dates
    # primary_ticker = input("Enter primary company ticker (e.g., AACG): ").upper()
    # start_date = input("Enter start date (e.g., Jan 01, 2023): ").title()
    # end_date = input("Enter end date (e.g., Jan 31, 2023): ").title()

    # Filter competitors for the given primary company
    competitors = competitors_df[competitors_df['company'] == primary_ticker]['competitors'].iloc[0].split(', ')

    # Read data from output.json
    with open('output.json', 'r') as file:
        data_list = json.load(file)

    # Initialize an empty DataFrame
    df = pd.DataFrame(columns=['Date'] + competitors)

    # Loop through each entry in data_list
    for entry in data_list:
        # Extract the date and company data
        date_data = entry.get("date", [])
        company_name = entry.get("company", "")
        close_price = entry.get("close_price", "")

        # If date_data is within the user-provided range and the company is in the competitors list, create a DataFrame for the current entry
        if date_data and start_date <= date_data <= end_date and company_name in competitors:
            # Check if the row for the current date already exists in the DataFrame
            if date_data not in df["Date"].values:
                df = df._append({"Date": date_data}, ignore_index=True)

            # Update the corresponding closing price for the current company and date
            df.loc[df["Date"] == date_data, company_name] = close_price

    # Fill NaN values with None for a cleaner output
    df = df.where(pd.notna(df), None)

    # Print the final DataFrame
    print(tabulate(df, headers='keys', tablefmt='grid'))

    # Fill NaN values with None for a cleaner output
    df = df.where(pd.notna(df), None)

    # Print the final DataFrame
    print(tabulate(df, headers='keys', tablefmt='grid'))

    # Ask the user if they want to save the report to Excel
    save_to_excel = input("Do you want to save the report to an Excel file? (yes/no): ").lower()

    if save_to_excel == 'yes':
        # Get the file name from the user
        file_name = input("Enter the Excel file name (e.g., report.xlsx): ")

        # Save the report to Excel
        save_report_to_excel(df, file_name)
        print(f"Report saved to {file_name}")

# Entry point of the script
if __name__ == "__main__":
    main()



# import pandas as pd
# from tabulate import tabulate
# import json
#
# # Read competitors data from Competitors.csv
# competitors_df = pd.read_csv('/Users/ajmalamir/Documents/New_yahoo_finance/Even_code Request/yahoo_finance/yahoo_finance/spiders/Comepititors.csv')
#
# # Get user-provided primary company and start/end dates
# primary_ticker = input("Enter primary company ticker (e.g., AACG): ").upper()
# start_date = input("Enter start date (e.g., Jan 01, 2023): ").title()
# end_date = input("Enter end date (e.g., Jan 31, 2023): ").title()
#
# # Filter competitors for the given primary company
# competitors = competitors_df[competitors_df['company'] == primary_ticker]['competitors'].iloc[0].split(', ')
#
# # Read data from output.json
# with open('output.json', 'r') as file:
#     data_list = json.load(file)
#
# # Initialize an empty DataFrame
# df = pd.DataFrame(columns=['Date'] + competitors)
#
# # Loop through each entry in data_list
# for entry in data_list:
#     # Extract the date and company data
#     date_data = entry.get("date", [])
#     company_name = entry.get("company", "")
#     close_price = entry.get("close_price", "")
#
#     # If date_data is within the user-provided range and the company is in the competitors list, create a DataFrame for the current entry
#     if date_data and start_date <= date_data <= end_date and company_name in competitors:
#         # Check if the row for the current date already exists in the DataFrame
#         if date_data not in df["Date"].values:
#             df = df._append({"Date": date_data}, ignore_index=True)
#
#         # Update the corresponding closing price for the current company and date
#         df.loc[df["Date"] == date_data, company_name] = close_price
#
# # Fill NaN values with None for a cleaner output
# df = df.where(pd.notna(df), None)
#
# # Print the final DataFrame
# print(tabulate(df, headers='keys', tablefmt='grid'))









