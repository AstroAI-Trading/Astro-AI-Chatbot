from time import sleep
from azure_storage_code.upload_data import Azure
from os import getenv
from dotenv import load_dotenv
from subprocess import run
from platform import system
import azure_storage_code.data_extraction as extract
from scrapy.crawler import CrawlerProcess
from fred_scraping.fred_scraping.spiders.astro_spider import AstroSpider
from YahooScraping.yahoo_finance.spiders.yahoo_astro_spider import YahooFinanceSpider
from sys import exit
from urllib.parse import urlparse
from nbformat import read
from nbconvert import PythonExporter
from pathlib import Path
from requests import get
from linear_regression.Files_for_Priming_Sector_Comps import comp_momentum, DCF2
import pandas as pd
from collections import OrderedDict


'''
For Linear Regression (Call Second):
Start with FMP
DCF2
SectorData
Regression
'''

'''
For macro (Call first):
macro_test
DCF_assumptions
'''

'''
Scrape first
Then call macro
Then call linear regression
Call momentum
Call DCF_assumptions
Call DCF2
'''


def execute_notebook(notebook_path: Path) -> None:
    if not notebook_path.is_file():
        exit('The file path to the notebook does not exist. Ensure that it does before running the program again.')

    with open(notebook_path, 'r', encoding='utf-8') as notebook_file:
        notebook_content = read(notebook_file, as_version=4)

    python_exporter = PythonExporter()

    python_script, _ = python_exporter.from_notebook_node(notebook_content)

    exec(python_script)


def check_scraping_link(link: str) -> bool:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = get(link, headers=headers)
        print(f"Checking URL: {link} - Status Code: {response.status_code}")
        return response.ok
    except Exception as e:
        print(f"Error checking URL: {link} - Error: {e}")
        return False



def scraping_specified_link(link: str) -> None:
    domain = urlparse(link).hostname

    # Determine the appropriate spider based on the domain
    if 'yahoo.com' in domain:
        spider = YahooFinanceSpider
    elif 'fred.stlouisfed.org' in domain:
        spider = AstroSpider
    else:
        print(f"Invalid URL: {link}")
        return

    # Run the Scrapy spider without checking the URL
    process = CrawlerProcess()
    process.crawl(spider, start_url=link)
    process.start()

    print(f"Scraping completed for URL: {link}")



def upload(storage_upload: Azure, iterations: int):
    if iterations == 0:
        print('You entered 0 iterations. Will not upload any files.')
        return
    while iterations > 0:
        file_path = Azure.path_function_upload()
        if file_path is None:
            print('An invalid file path was entered. Cannot upload the file.')
            iterations -= 1
            continue

        container_name_upload = Azure.container_function()
        storage_upload.upload_file(file_path, container_name_upload, file_path.name)
        iterations -= 1
        if iterations > 0:
            print('Will begin to upload the next file shortly.')

        sleep(3.5)


def download(storage_download: Azure, iterations: int) -> None:
    if iterations == 0:
        print('You entered 0 iterations. Will not download any files.')
        return

    sas_token_recorded = False
    sas_token = ''

    while iterations > 0:
        blob_name_download = Azure.blob_function()
        container_name_download = Azure.container_function()
        destination_path = Azure.path_function_download()
        if not sas_token_recorded:
            # Here in case if the user doesn't have an SAS Token already created
            need_token = True
            sas_prompt = input('Do you have an SAS Token? (y/n) Default n: ')
            if sas_prompt.lower() == 'y':
                sas_entered = False
                while not sas_entered:
                    sas_token = input('Enter your SAS Token: ')
                    if sas_token and not sas_token.isspace():
                        sas_entered = True

                # Basically means if the function returns false meaning if the SAS Token is invalid
                need_token = not Azure.sas_token_valid(sas_token, container_name_download)

                print(
                    'You entered an invalid SAS Token. One will be created for you.' if need_token else 'You entered a valid token. It will be used to download the file(s).')

            if need_token:
                sas_token = storage_download.generate_sas(container_name_download, blob_name_download)
                if sas_token is None:
                    # Something went wrong if the code goes here.
                    print("An SAS Token couldn't be generated. Exiting now.")
                    break

            sas_token_recorded = True

        storage_download.download_file(container_name_download, sas_token, blob_name_download, destination_path)

        iterations -= 1
        if iterations > 0:
            print('Proceeding to download the next file.')

        sleep(3.5)


def parse_files() -> None:
    files = input('Enter the files you want to parse. Separate them by spaces and include the correct file paths: ')
    sleep(1.5)
    if not Azure.check_files(files.split()):
        print("At least one of the files entered doesn't exist. Cannot continue.")
        return

    extract.parse_files(files.split())


# This function is meant to be used outside of manager.py so time doesn't have to be imported in each file
def program_sleep(seconds: float) -> None:
    sleep(seconds)


def clear_terminal() -> None:
    system_platform = system()
    run('cls' if system_platform == 'Windows' else 'clear', shell=True)


if __name__ == '__main__':
    try:
        load_dotenv(override=True, verbose=True)
        client_id = getenv('client_id')
        client_secret = getenv('client_secret')
        tenant_id = getenv('tenant_id')
        redirect_uri = getenv('redirect_uri')
        application_uri = getenv('application_uri')
        api_base_url = getenv('api_base_url')
        subscription_id = getenv('subscription_id')
        connection_string = getenv('connection_string')
        account_key = getenv('account_key')
    except Exception as e:
        print(f'Could not find all env variables {e}')
        exit(1)

    storage = Azure(client_id_var=client_id, client_secret_var=client_secret, tenant_id_var=tenant_id,
                    redirect_uri_var=redirect_uri, application_uri_var=application_uri, api_base_url_var=api_base_url,
                    subscription_id_var=subscription_id, connection_string_var=connection_string,
                    account_key_var=account_key)

    if not storage.authorize():
        exit("Couldn't authorize the app.")

    sleep(1.5)
    clear_terminal()
    print('Hello, welcome to the Astro-AI Chatbot.')
    sleep(0.3)
    print("We're happy you're here.")
    sleep(0.7)
    while True:
        
        # Need the options list for providing an easy way to select an option
        stock_ticker = input('Enter in a stock ticker or type q to quit: ')
        if stock_ticker.lower() == 'q':
            exit('Thank you for using the Astro-AI Chatbot.')
        sleep(0.5)
        '''
        # Call scrape step is checked
        scraping_specified_link(f'https://finance.yahoo.com/quote/{stock_ticker}/financials?p={stock_ticker}')
        sleep(0.5)
        macro_notebook_path = './macro/macro_test.ipynb'
        # Macro step is checked
        execute_notebook(Path(macro_notebook_path).absolute().resolve())
        sleep(0.4)
        regression_notebook_path = './linear_regression/Files_for_Priming_Sector_Comps/Regression.ipynb'
        # Called Regression Here
        execute_notebook(Path(regression_notebook_path).absolute().resolve())
        sleep(0.4)
        # Called momentum here. Keep in mind it's temporary
        comp_momentum.main()
        '''
        dcf_assumptions_path = './macro/DCF_assumptions.ipynb'
        # Executed dcf assumptions here
        execute_notebook(Path(dcf_assumptions_path).absolute().resolve())
        sleep(0.3)
        # Execute DCF2
        DCF2.main()

        '''
        Someone needs to test this code out as the nbcovert library is not working
        on my machine, and I couldn't find a solution from chatgpt nor the google. I need to know if this is 
        a me issue or a library issue.
        '''