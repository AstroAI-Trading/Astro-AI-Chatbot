# urls.py

fred_urls = [
    'https://fred.stlouisfed.org/series/CORESTICKM159SFRBATL',
    # 'https://fred.stlouisfed.org/series/T5YIFR',
    # 'https://fred.stlouisfed.org/series/T10Y2Y',
    # 'https://fred.stlouisfed.org/series/T10Y3M',
    # 'https://fred.stlouisfed.org/series/BAA10Y',
    # 'https://fred.stlouisfed.org/series/T3MFF',
    # 'https://fred.stlouisfed.org/series/SP500',
    # 'https://fred.stlouisfed.org/series/BOGZ1FL075035223Q',
    # 'https://fred.stlouisfed.org/series/DFF',
    # 'https://fred.stlouisfed.org/series/REAINTRATREARAT10Y',
    # 'https://fred.stlouisfed.org/series/MORTGAGE30US',
    # 'https://fred.stlouisfed.org/series/DJIA'
    
    # Add other FRED URLs as needed
]

yahoo_finance_urls = [
    # 'https://finance.yahoo.com/quote/GOOG/history?p=GOOG',
    # Add other Yahoo Finance URLs as needed
]

# sort_data.py
import json

def sort_and_store_json(input_file, output_file):
    try:
        # Load data from the original JSON file as a list of objects
        with open(input_file, 'r') as file:
            data = list(json.JSONDecoder().raw_decode(file.read())[0])
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{input_file}'")
        return

    # Check if there is data in the file
    if not data:
        print(f"Error: No data found in '{input_file}'")
        return

    # Check if the dictionaries in data have at least three elements
    if any(len(x) < 3 for x in data):
        print("Error: Some dictionaries in the data do not have at least three elements.")
        return

    # Sort data based on the values of the third column
    sorted_data = sorted(data, key=lambda x: float(list(x.values())[2]))

    # Store the sorted data in a new JSON file
    with open(output_file, 'w') as file:
        json.dump(sorted_data, file, indent=2)

    print(f"Data sorted and stored in '{output_file}'")


# Example usage:
# sort_and_store_json('original_data.json', 'sorted_data.json')
