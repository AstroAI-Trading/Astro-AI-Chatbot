import data_extraction as extract
import pandas as pd
import os
from dotenv import load_dotenv
import logging
import sys
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from msal import ConfidentialClientApplication
from datetime import datetime, timedelta
import re
from pathlib import Path
from urllib.parse import quote

class azure:

    def __init__(self, client_id=None, client_secret=None, tenant_id=None, redirect_uri=None, application_uri=None, api_base_url=None, subscription_id=None, connection_string=None, account_key=None) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.redirect_uri = redirect_uri
        self.application_uri = application_uri
        self.access_token = None
        self.api_base_url = api_base_url
        self.subscription_id = subscription_id
        self.connection_string = connection_string
        self.account_key = account_key
        
    
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    def authorize(self) -> bool:
        '''
        Authorizes the app to use Azure\n
        Returns true if successful, false otherwise
        '''
        app = ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=f'https://login.microsoftonline.com/{self.tenant_id}'
        )

        accounts = app.get_accounts()
        if accounts:
            print('Pick the account you want to use to proceed.\n')
            for a in accounts:
                print(a['username'])
                print('\n')
            
            choice = input('Account: ')

            self.access_token = app.acquire_token_silent(scopes=[f'{self.application_uri}/.default'], account=choice)
            return True
        else:
            self.access_token = app.acquire_token_for_client(scopes=[f'{self.application_uri}/.default'])

            if 'access_token' in self.access_token:
                print(f"Here is your access token: {self.access_token['access_token']}\n")
                return True
            else:
                print(self.access_token.get('error'))
                print(self.access_token.get('error_description'))
                print(self.access_token.get('correlation_id'))
                return False

    def upload_file(self, file_path: Path, container_name: str, blob_name: str) -> None:
        '''
        Meant for having a file you want to upload to the Onedrive.\n
        file_path: The file on your local machine that you want to upload.\n
        connection_string: The string that is used to authenticate and connect to the azure storage account.\n
        container_name: The name of the container on azure in which you want to upload the file.\n
        blob_name: The desired name you want for the file when it's uploaded
        '''
        if not self.access_token:
                print('Access Token is missing. You need to authorize the app first.')
        else:
            try:

                blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
                container_client = blob_service_client.get_container_client(container_name)

                with open(file_path, 'rb') as data:
                    container_client.upload_blob(name=blob_name, data=data)
                
                print(f'File {file_path} uploaded to Azure Storage Container {container_name} as {blob_name}.')
            except Exception as e:
                print(f'Could not successfully upload file to the Azure Storage Account {e}')

    def generate_sas(self, container_name: str, blob_name: str) -> str | None:
        '''
        Generates an SAS Token that will give you permission to download a file from the storage account\n
        Returns the token if successful; returns None if something went wrong
        '''

        if not self.account_key:
            print('Account key is missing. Cannot generate SAS token.')
            return None

        blob_service_client = BlobServiceClient(account_url=f"https://astroaitrading.blob.core.windows.net", credential=self.account_key)
        permissions = BlobSasPermissions(read=True, write=True)
        expiry = datetime.utcnow() + timedelta(days=1)

        sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            container_name=container_name,
            blob_name=blob_name,
            permission=permissions,
            expiry=expiry,
            account_key=self.account_key
        )

        if sas_token is None:
            print('Could not generate an SAS Token. Cannot proceed with the download.')
            return None
        else:
            print(f'Here is your SAS Token. It will be good for 1 day {sas_token}')
            return str(sas_token)


    def download_file(self, container_name: str, sas_token: str, blob_name: str, destination_path: Path) -> None:
        '''
        Download a file that already exists on onedrive.\n
        connection_string: The string that is used to authenticate and connect to the azure storage account.\n
        container_name: The name of the container on azure in which you want to download the file from.\n
        blob_name: The name of the file on Azure you want to download.\n
        destination_path: The path on your local machine where you want to store the file once it's downloaded
        '''
        if not self.access_token:
            print('Access Token is missing. You need to authorize the app first.')
        else:
            try:
                
                sas_token = quote(sas_token)

                blob_service_client = BlobServiceClient.from_connection_string(f"{self.connection_string}?{sas_token}")
                blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

                file_path = destination_path / blob_name

                file_path.parent.mkdir(parents=True, exist_ok=True)

                with open(file_path, 'wb') as file:
                    data = blob_client.download_blob()
                    file.write(data.readall())
                
                print(f'File downloaded from Azure Storage Container {container_name} as {destination_path}.')
            except Exception as e:
                print(f'Could not download file from Azure Storage Container {e}')


    def upload_dataframe(self, dataframe: pd.DataFrame, container_name: str, blob_name: str, file_format: str) -> None:
        '''
        Meant for uploading a Pandas Dataframe a user might have.\n
        connection_string: The string that is used to authenticate and connect to the azure storage account.\n
        container_name: The name of the container on azure in which you want to upload the file.\n
        blob_name: The name of the file on Azure you want it to be when it is uploaded.\n
        file_format: The type of the file. Examples include word or powerpoint.
        '''
        if not self.access_token:
            print('Access Token is missing. You need to authorize the app first.')
        else:
            try:

                if file_format == 'csv':
                    file_content = dataframe.to_csv(index=False).encode()
                elif file_format == 'excel':
                    file_content = dataframe.to_excel(index=False)
                else:
                    print('Did not specify csv or excel. Cannot continue')
                    return

                blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
                container_client = blob_service_client.get_container_client(container_name)

                with container_client.get_blob_client(blob_name) as blob_client:
                    blob_client.upload_blob(file_content, blob_type='BlockBlob')

                print(f'Dataframe uploaded to Azure Storage Container {container_name} as {blob_name}.')
            except Exception as e:
                print(f'Could not upload dataframe to Azure Storage Container {e}')
    
    # Every method below will be static
    @staticmethod
    def blob_function() -> str:
        blob_name = input("Enter the desired name of the file when it's uploaded or the name of the file you want to download: ")
        # re.search checks to see if any letters were entered
        if not blob_name or not re.search('[a-zA-Z]+', blob_name):
            print('Empty or invalid name. The name will be file.txt')
            blob_name = 'file.txt'
        
        blob_name = blob_name.replace(" ","")

        # This function seprates the name of the file with the extension
        '''
        root, extension = os.path.splitext(blob_name)

        if not extension or extension == '.':
            extension_input = input('An extension was not provided. Please enter one: ')
            if not extension_input or extension_input == '.' or not re.search('^\.[a-zA-Z]+$', extension_input):
                print('An extension was not properly entered. The extension will be .txt')
                extension_input = '.txt'
 
            extension_input = extension_input.replace(' ','')
            blob_name = root + extension_input
        '''

        blob_path = Path(blob_name)

        while not blob_path.suffix or blob_path.suffix.isspace() or blob_path.suffix == '.':
            blob_path.suffix = input('An extension was not provided. Please enter one: ')
        
        invalid_chars = r'\/:*?"<>|'
        blob_path_str = str(blob_path)
        # Translates each invalid character to empty
        blob_path_str = blob_path_str.translate(str.maketrans('','', invalid_chars))
        return blob_path_str
        
    @staticmethod
    def container_function() -> str:
        container_name_pattern = re.compile(r'^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$')
        container_name = ''
        while not container_name_pattern.match(container_name):
            container_name = input('Please enter the name of the container on your Azure Storage Account you want to use: ')

        return container_name

        '''
        container_incomplete = True
        while container_incomplete:
            container_name = input('Enter the name of the container on your azure storage account that you want to upload or download the file: ')
            if not container_name or container_name.isspace():
                print('A container name was not entered. Try again.')
                container_incomplete = True
            else:
                container_incomplete = False
        return container_name
        '''
            
    @staticmethod
    def path_function_upload() -> Path | None:
        try:
            while True:
                directory_path = input('Enter the directory path to the file that will be uploaded. Do not include the file name: ')
                file_name = input('Enter the name of the file you want to upload: ')

                path = Path(directory_path).joinpath(file_name)

                if path.is_file():
                    break
                else:
                    print("Path doesn't point to an existing file. Try again.")
                    continue

            return path.resolve(strict=True)
        
        except FileNotFoundError as f:
            print(f"The path doesn't exist {f}")
            return None


    @staticmethod
    def path_function_download() -> Path:
        directory_path_pattern = re.compile(r'^([a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*\\?$|/(?:[^\\/:*?"<>|\r\n]+/)*[^\\/:*?"<>|\r\n]*/?)$')

        while True:
            path_str = input('Enter the path to the directory you want the files to be downloaded to: ')
            
            if directory_path_pattern.search(path_str):
                break
            else:
                print('Invalid directory path. Please try again.')
                continue
        
        path = Path(path_str)

        return path.resolve()

    @staticmethod
    def check_files(files_list: list[str]) -> bool:

        if not files_list:
            print('There are no files to check. Ending Operation.')
            return False

        files_cleared = True

        for file in files_list:
            file_path = Path(file).resolve()

            if file_path.is_file():
                files_cleared = True
            else:
                files_cleared = False
                break
        
        if files_cleared:
            return True
        else:
            return False
    
    @staticmethod
    def create_dataframe(files_dataframe: list[str]) -> pd.DataFrame | None:
        data_list = []
        for file in files_dataframe:
            file_extension = Path(file).suffix.lower()
            if file_extension == '.csv':
                data = pd.read_csv(file)
            elif file_extension in ('.xls', '.xlsx', '.xlsm', '.xlsb'):
                data = pd.read_excel(file)
            elif file_extension == '.json':
                data = pd.read_json(file)
            elif file_extension in ('.html', '.htm'):
                data = pd.read_html(file)
                if isinstance(data, list):
                    data = pd.concat(data)
            elif file_extension == '.xml':
                data = pd.read_xml(file)
            else:
                print(f'Skipping invalid file {file}')
            data_list.append(data)
        
        if not data_list:
            print('No data was found to create a dataframe. Cannot continue.')
            return None
        
        return pd.concat(data_list, ignore_index=True)


if __name__ == '__main__':
    try:
        load_dotenv(override=True, verbose=True)
        client_id = os.getenv('client_id')
        client_secret = os.getenv('client_secret')
        tenant_id = os.getenv('tenant_id')
        redirect_uri = os.getenv('redirect_uri')
        application_uri = os.getenv('application_uri')
        api_base_url = os.getenv('api_base_url')
        subscription_id = os.getenv('subscription_id')
        connection_string = os.getenv('connection_string')
        account_key = os.getenv('account_key')
    except Exception as e:
        print(f'Could not find all env variables {e}')
        sys.exit(1)
    
    storage = azure(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id, redirect_uri=redirect_uri, application_uri=application_uri, api_base_url=api_base_url, subscription_id=subscription_id, connection_string=connection_string, account_key=account_key)

    if not storage.authorize():
        print('Authorization failed. Exiting.')
        sys.exit(1)
    else:

        while True:
            
            options = ['Upload File', 'Download File', 'Upload Dataframe', 'Parse Files', 'Exit']

            print('Select from the following options. Enter the number associated with it.\n')
            for i, option in enumerate(options, start=1):
                print(f'{i}\t{option}')
            
            try:
                choice = int(input('Option: '))
            except ValueError:
                print('Input is not a number. Try again.')
                continue

            if 1 <= choice <= len(options):
                selected_option = options[choice - 1]

                match selected_option:
                    case 'Upload File':
                        blob_name = azure.blob_function()
                        container_name = azure.container_function()
                        file_path = azure.path_function_upload()

                        if file_path is not None:
                            storage.upload_file(file_path, container_name, blob_name)

                    case 'Download File':
                        blob_name = azure.blob_function()
                        container_name = azure.container_function()
                        destination_path = azure.path_function_download()

                        token_exists = input('Do you have an SAS Token? (y/n) Default is n: ')

                        if token_exists.lower() == 'y':
                            token_entered = False
                            while not token_entered:
                                sas_token = input('Enter your SAS Token: ')
                                if not sas_token or sas_token.isspace():
                                    print("SAS Token wasn't entered. Try again.")
                                    token_entered = False
                                else:
                                    token_entered = True
                        else:
                            sas_token = storage.generate_sas(container_name, blob_name)
                            if sas_token is None:
                                print('An SAS Token could not be generated. Cannot proceed with downloading the file.')
                                           
                        storage.download_file(container_name, sas_token, blob_name, destination_path)

                    case 'Upload Dataframe':
                        blob_name = azure.blob_function()
                        container_name = azure.container_function()
                        files = input('Enter the files you want to convert to a dataframe then uploaded. Separate them by spaces and include the correct paths: ')
                        if not azure.check_files(files.split()):
                            print('Not all the files exist. Cannot continue.')
                        else:
                            dataframe = azure.create_dataframe(files.split())
                            if dataframe is not None:
                                file_format = input('Do you want to parse the dataframe into a csv or excel file? Enter csv or excel all lowercase: ')
                                storage.upload_dataframe(dataframe, container_name, blob_name, file_format)
                            else:
                                print("Not able to convert files in a pandas dataframe. Sorry :(")
            
                    case 'Parse Files':
                        files = input('Enter the files you want to parse. Separate them by spaces and include the correct paths: ')

                        if azure.check_files(files.split()):
                            extract.parse_files(files.split())
                        else:
                            print('Not all the files exist. Cannot continue.')

                    case 'Exit':
                        print('Exiting program. Goodbye!')
                        sys.exit(0)
            else:
                print('Invalid number. Try Again.')