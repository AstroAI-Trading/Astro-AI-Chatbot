import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

import pandas as pd
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from msal import ConfidentialClientApplication
from azure.core.exceptions import ResourceNotFoundError


class Azure:

    def __init__(self, client_id_var=None, client_secret_var=None, tenant_id_var=None, redirect_uri_var=None,
                 application_uri_var=None, api_base_url_var=None, subscription_id_var=None, connection_string_var=None,
                 account_key_var=None) -> None:
        self.client_id = client_id_var
        self.client_secret = client_secret_var
        self.tenant_id = tenant_id_var
        self.redirect_uri = redirect_uri_var
        self.application_uri = application_uri_var
        self.access_token = None
        self.api_base_url = api_base_url_var
        self.subscription_id = subscription_id_var
        self.connection_string = connection_string_var
        self.account_key = account_key_var

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    def authorize(self) -> bool:
        """
        Authorizes the app to use Azure\n
        Returns true if successful, false otherwise
        """
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

    def upload_file(self, file_path: Path, container_name_upload: str, blob_name_upload: str) -> None:
        """
        Meant for having a file you want to upload to the Onedrive.\n
        file: The file on your local machine that you want to upload.\n
        connection_string: The string that is used to authenticate and connect to the azure storage account.\n
        container_name: The name of the container on azure in which you want to upload the file.\n
        blob_name: The desired name you want for the file when it's uploaded
        """
        if not self.access_token:
            print('Access Token is missing. You need to authorize the app first.')
        else:
            try:
                blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
                container_client = blob_service_client.get_container_client(container_name_upload)

                with open(file_path, 'rb') as data:
                    container_client.upload_blob(name=blob_name_upload, data=data)

                print(
                    f'File {blob_name_upload} uploaded to Azure Storage Container {container_name_upload}.')
            except Exception as e:
                print(f'Could not successfully upload file to the Azure Storage Account {e}')

    def generate_sas(self, container_name_sas: str, blob_name_sas: str) -> str | None:
        """
        Generates an SAS Token that will give you permission to download a file from the storage account\n
        Returns the token if successful; returns None if something went wrong
        """

        if not self.account_key:
            print('Account key is missing. Cannot generate SAS token.')
            return None

        blob_service_client = BlobServiceClient(account_url=f"https://astroaitrading.blob.core.windows.net",
                                                credential=self.account_key)
        permissions = BlobSasPermissions(read=True, write=True)
        expiry = datetime.utcnow() + timedelta(days=1.0)

        sas_token = generate_blob_sas(
            account_name=blob_service_client.account_name,
            container_name=container_name_sas,
            blob_name=blob_name_sas,
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

    @staticmethod
    def sas_token_valid(sas_token: str, container_name_valid: str) -> bool:
        try:
            blob_service_client = BlobServiceClient(account_url='https://astroaitrading.blob.core.windows.net',
                                                    credential=sas_token)
            container_client = blob_service_client.get_container_client(container=container_name_valid)
            container_client.get_container_properties(container_name_valid)
            return True
        except ResourceNotFoundError:
            return False

    def download_file(self, container_name_download: str, sas_token_download: str, blob_name_download: str,
                      destination_path_download: Path) -> None:
        """
        Download a file that already exists on onedrive.\n
        connection_string: The string that is used to authenticate and connect to the azure storage account.\n
        container_name: The name of the container on azure in which you want to download the file from.\n
        blob_name: The name of the file on Azure you want to download.\n
        destination_path: The path on your local machine where you want to store the file once it's downloaded
        """
        if not self.access_token:
            print('Access Token is missing. You need to authorize the app first.')
        else:
            try:

                sas_token_download = quote(sas_token_download)

                blob_service_client = BlobServiceClient.from_connection_string(
                    f"{self.connection_string}?{sas_token_download}")
                blob_client = blob_service_client.get_blob_client(container=container_name_download,
                                                                  blob=blob_name_download)

                file_path_download = destination_path_download / blob_name_download

                file_path_download.parent.mkdir(parents=True, exist_ok=True)

                with open(file_path_download, 'wb') as file:
                    data = blob_client.download_blob()
                    file.write(data.readall())

                print(
                    f'File downloaded from Azure Storage Container {container_name_download} as {destination_path_download}.')
            except Exception as download_error:
                print(f'Could not download file from Azure Storage Container {download_error}')

    def upload_dataframe(self, dataframe_upload: pd.DataFrame, container_name_dataframe: str, blob_name_dataframe: str,
                         file_format_dataframe: str) -> None:
        """
        Meant for uploading a Pandas Dataframe a user might have.\n
        connection_string: The string that is used to authenticate and connect to the azure storage account.\n
        container_name: The name of the container on azure in which you want to upload the file.\n
        blob_name: The name of the file on Azure you want it to be when it is uploaded.\n
        file_format: The type of the file. Examples include word or PowerPoint.
        """
        if not self.access_token:
            print('Access Token is missing. You need to authorize the app first.')
        else:
            try:

                if file_format_dataframe == 'csv':
                    file_content = dataframe_upload.to_csv(index=False).encode()
                elif file_format_dataframe == 'excel':
                    dataframe_upload.to_excel(index=False)
                else:
                    print('Did not specify csv or excel. Cannot continue')
                    return

                blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
                container_client = blob_service_client.get_container_client(container_name_dataframe)

                with container_client.get_blob_client(blob_name_dataframe) as blob_client:
                    blob_client.upload_blob(file_content, blob_type='BlockBlob')

                print(
                    f'Dataframe uploaded to Azure Storage Container {container_name_dataframe} as {blob_name_dataframe}.')
            except Exception as e:
                print(f'Could not upload dataframe to Azure Storage Container {e}')

    # Every method below will be static
    @staticmethod
    def blob_function() -> str:
        blob_name_input = input(
            "Enter the desired name of the file when it's uploaded or the name of the file you want to download: ")
        # re.search checks to see if any letters were entered
        if not blob_name_input or not re.search('[a-zA-Z]+', blob_name_input):
            print('Empty or invalid name. The name will be file.txt')
            blob_name_input = 'file.txt'

        blob_name_input = blob_name_input.replace(" ", "")

        # This function separates the name of the file with the extension
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

        blob_path = Path(blob_name_input)

        while not blob_path.suffix or blob_path.suffix.isspace() or blob_path.suffix == '.':
            blob_path.suffix = input('An extension was not provided. Please enter one: ')

        invalid_chars = r'\/:*?"<>|'
        blob_path_str = str(blob_path)
        # Translates each invalid character to empty
        blob_path_str = blob_path_str.translate(str.maketrans('', '', invalid_chars))
        return blob_path_str

    @staticmethod
    def container_function() -> str:
        container_name_pattern = re.compile(r'^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$')
        container_name_input = ''
        while not container_name_pattern.match(container_name_input):
            container_name_input = input(
                'Please enter the name of the container on your Azure Storage Account you want to use: ')

        return container_name_input

    @staticmethod
    def path_function_upload() -> Path | None:
        try:
            while True:
                directory_path = input(
                    'Enter the directory path to the file that will be uploaded. Do not include the file name: ')
                file_name = input('Enter the name of the file you want to upload: ')

                path = Path(directory_path).joinpath(file_name)

                if path.is_file():
                    break
                else:
                    print("Path doesn't point to an existing file. Try again.")
                    continue

            return path.resolve(strict=True)

        except FileNotFoundError:
            return None

    @staticmethod
    def path_function_download() -> Path:
        directory_path_pattern = re.compile(
            r'^([a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*\\?$|/(?:[^\\/:*?"<>|\r\n]+/)*[^\\/:*?"<>|\r\n]*/?)$')

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
            file_path_check = Path(file).resolve()

            if not file_path_check.is_file():
                files_cleared = False
                break

        return files_cleared

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
