from time import sleep
from azure_storage_code.upload_data import Azure
from os import getenv
from dotenv import load_dotenv
from subprocess import run
from platform import system
import azure_storage_code.data_extraction as extract
import requests
from scrapy.crawler import CrawlerProcess
from fred_scraping.fred_scraping.spiders.astro_spider import AstroSpider
from YahooScraping.yahoo_finance.spiders.yahoo_astro_spider import YahooFinanceSpider
from sys import exit


def scrape():
    return


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
            need_token = True
            sas_prompt = input('Do you have an SAS Token? (y/n) Default n: ')
            if sas_prompt.lower() == 'y':
                sas_entered = False
                while not sas_entered:
                    sas_token = input('Enter your SAS Token: ')
                    if sas_token and not sas_token.isspace():
                        sas_entered = True

                need_token = not Azure.sas_token_valid(sas_token, container_name_download)

                print(
                    'You entered an invalid SAS Token. One will be created for you.' if need_token else 'You entered a valid token. It will be used to download the file(s).')

            if need_token:
                sas_token = storage_download.generate_sas(container_name_download, blob_name_download)
                if sas_token is None:
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


def linear_regression() -> None:
    return


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
        print("Couldn't authorize the app.")
        exit(1)

    sleep(2.5)
    clear_terminal()
    print('Hello, welcome to the Astro-AI Chatbot.')
    sleep(2.5)
    print("We're happy you're here.")
    sleep(1.5)
    while True:
        options = ['Scrape Data', 'Upload Data', 'Download File', 'Parse Files', 'Perform Linear Regression', 'Exit']
        print('Please choose an option by typing in the number associated with it.')
        for i, option in enumerate(options, start=1):
            print(f'{i}\t{option}')

        try:
            choice = int(input('Option: '))
        except ValueError:
            print('A whole number was not entered. Please try again.')
            continue

        sleep(2.5)
        if 1 <= choice <= len(options):
            match choice:
                case 1:
                    print('Will scrape data here.')
                case 2:
                    try:
                        iterations_upload = int(input('How many times will you be uploading a file: '))
                    except ValueError:
                        print('A whole number was not entered. The amount of iterations will be 1.')
                        iterations_upload = 1
                    upload(storage, iterations_upload)
                case 3:
                    try:
                        iterations_download = int(input("Enter how many time you'll be downloading a file: "))
                    except ValueError:
                        print("A whole number wasn't entered. The amount of iterations will be 1.")
                        iterations_download = 1
                    download(storage, iterations_download)
                case 4:
                    parse_files()
                case 5:
                    linear_regression()
                case 6:
                    print('Exiting the program. Thank you for using the Astro-AI Chatbot.')
                    exit(0)
        else:
            print('Invalid Number. Try again.')
            continue

        sleep(2.5)
        clear_terminal()
