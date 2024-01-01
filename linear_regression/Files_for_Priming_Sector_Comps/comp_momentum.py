# import pandas as pd
# import numpy as np 


# ### These will all be seperate DFs with the daily closing prices of these companies

# OG_COMPANY = 'TICKER HERE'
# COMP1 = 'TICKER HERE'
# COMP2 = 'TICKER HERE'
# COMP3 = 'TICKER HERE'
# COMP4 = 'TICKER HERE'
# COMP5 = 'TICKER HERE'
# COMP6 = 'TICKER HERE'
# COMP7 = 'TICKER HERE'
# COMP8 = 'TICKER HERE'
# COMP9 = 'TICKER HERE'
# COMP10 = 'TICKER HERE'

# combined_df = pd.merge(OG_COMPANY, COMP1, on='Date', how='outer')
# combined_df = pd.merge(combined_df, COMP2, on='Date', how='outer')
# combined_df = pd.merge(combined_df, COMP3, on='Date', how='outer')
# combined_df = pd.merge(combined_df, COMP4, on='Date', how='outer')
# combined_df = pd.merge(combined_df, COMP5, on='Date', how='outer')
# combined_df = pd.merge(combined_df, COMP6, on='Date', how='outer')
# combined_df = pd.merge(combined_df, COMP7, on='Date', how='outer')
# combined_df = pd.merge(combined_df, COMP8, on='Date', how='outer')
# combined_df = pd.merge(combined_df, COMP9, on='Date', how='outer')
# combined_df = pd.merge(combined_df, COMP10, on='Date', how='outer')


import pandas as pd


def reverse_dataframe(df):
    """
    Reverse the DataFrame so that the most recent dates are first.
    """
    return df.iloc[::-1].reset_index(drop=True)


def convert_to_numeric(df, date_column='Date'):
    """
  Convert non-numeric values in specified columns to NaN (except for the first row).
  """
    for col in df.columns:
        if col != date_column:
            df[col] = pd.to_numeric(df[col][1:], errors='coerce')
    return df


def calculate_pct_change(df, periods):
    """
    Calculate the percentage change for the given number of periods,
    starting from the second row, and raise an error if non-numeric data is found.
    """
    if not pd.api.types.is_numeric_dtype(df.iloc[:, 1:].dtypes):
        raise TypeError(
            f"Non-numeric data found in columns: {df.columns[1:]}. Please check and rectify before calculating percentage change.")
    return df.iloc[1:].pct_change(periods) * 100


def calculate_weekly_change(df):
    """
    Calculate the weekly percentage change for the 'MVST Close' column after data validation.
    """
    return calculate_pct_change(df[["Date", "MVST Close"]], 5)


def main() -> None:
    # Load your DataFrame (replace 'file_path' with the actual path)
    # file_path = '/Users/evan/Desktop/chatbot/Regression Testing/venv/bin/MergeManipulationsFMP/Components/MVST_daily.xlsx'
    file_path = '..\\Astro-AI-Chatbot\\linear_regression\\Files_for_Priming_Sector_Comps\\MVST_2022_FY_RUNINNG.xlsx'
    df = pd.read_excel(file_path)
    df['MVST Close'] = pd.to_numeric(df['MVST Close'], errors='raise', downcast='float')

    # Convert 'MVST Close' column to numeric (excluding headers)
    df = convert_to_numeric(df.copy()) 

    # Reverse the DataFrame for easier analysis
    reversed_df = reverse_dataframe(df)

    # Calculate weekly percentage change for 'MVST Close'
    weekly_change = calculate_weekly_change(reversed_df)

    # Print weekly percentage change (you can adjust this to your needs)
    print("Weekly Percentage Change for MVST Close:")
    print(weekly_change["MVST Close"])

    # (Optional) Print information for debugging purposes
    print("\nData types after conversion:")
    print(df.dtypes)

    print("\nFirst few rows of data:")
    print(df.head())

    df['MVST Close'].describe()
