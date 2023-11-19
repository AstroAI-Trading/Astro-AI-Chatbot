import pandas as pd
from pathlib import Path
import re


def create_directory() -> Path:
    '''
    Function for creating the folder.\n
    Returns a Pathlib Path which is the name of the folder.
    '''
    directory_path_pattern = re.compile(r'^([a-zA-Z]:\\(?:[^\\/:*?"<>|\r\n]+\\)*[^\\/:*?"<>|\r\n]*\\?$|/(?:[^\\/:*?"<>|\r\n]+/)*[^\\/:*?"<>|\r\n]*/?)$')

    while True:
        directory_path_str = input('Enter the directory path you want the parsed files to be located at: ')
        if directory_path_pattern.search(directory_path_str):
            return Path(directory_path_str).resolve()
        else:
            print("Invalid directory path. Please try again.")

def create_file() -> Path:
    '''
    Creates a file used to store the data.\n
    file_name: The name of the file. If none, will prompt you to enter one.\n
    Returns a Pathlib Path which is the name of the file.
    '''
    file_name_pattern = re.compile(r'^[a-zA-Z0-9_]+\.[a-zA-Z]{2,4}$')

    while True:
        file_name = input('Enter the name of the files you want the parsed file to be: ')
        if file_name_pattern.search(file_name):
            file_path = Path(file_name)
            if file_path.suffix != '.csv':
                file_path = file_path.with_suffix('.csv')
            return file_path.resolve()
        else:
            print('Invalid file name. Please try again.')

def parse_files(files: list) -> None:
    '''
    Parses multiple files into one csv File.\n
    '''
    if not files:
        print('There are no files to parse. Ending operation.')
        return 
    
    data_list = []

    try:
        for file in files:
            if isinstance(file, str):
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
                    print(f'Skipping unrecognized file type {file}')
                    continue

                data_list.append(data)
            else:
                print(f'Skipping non-string file {file}')
    except Exception as e:
        print(f'Error reading file {e}')
        return 
    
    if not data_list:
        print('Data list is empty. Cannot continue.')
        return 
    
    data_df = pd.concat(data_list, ignore_index=True)
    directory_name = create_directory()
    file_name = create_file()
    file_path = directory_name.joinpath(file_name)

    file_path.mkdir(parents=True, exist_ok=True)

    try:
        data_df.to_csv(file_path, index=False)
        print(f'Data saved to {file_path}')
    except Exception as e:
        print(f'Error saving data to {file_path}: {e}')