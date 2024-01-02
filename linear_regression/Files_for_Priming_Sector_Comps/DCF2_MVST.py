import pandas as pd
import numpy as np

# Load the financial data from the spreadsheet
file_path = '..\\Astro-AI-Chatbot\\linear_regression\\Files_for_Priming_Sector_Comps\\ANSS_2022_FY_.xlsx'
balance_sheet_sheet_name = 'CONSOLIDATED BALANCE SHEETS'
balance_sheet = pd.read_excel(file_path, sheet_name=balance_sheet_sheet_name)

# Extract 'Cash and cash equivalents' and 'Notes payable' for 2022
cash_and_equivalents_2022 = balance_sheet.iloc[1, 1]  # Update row index if needed
notes_payable_2022 = balance_sheet.iloc[19, 1]  # Update row index if needed

# Calculate net debt for 2022
net_debt = notes_payable_2022 - cash_and_equivalents_2022

# Constants - Replace these with your specific assumptions
REVENUE_GROWTH_RATE = 0.2
OPERATING_MARGIN = 0.2
TAX_RATE = 0.21
WACC = 0.0921
TERMINAL_GROWTH_RATE = 0.02
FORECAST_PERIOD = 10
num_shares = 8710000000


def load_financial_data(file_path, sheet_name='CONSOLIDATED STATEMENTS OF INCO'):
    income_statement = pd.read_excel(file_path, sheet_name=sheet_name)
    return income_statement


def forecast_cash_flows(income_statement, year):
    last_year_revenue = income_statement.iloc[2, 1]
    forecasted_revenue = last_year_revenue * (1 + REVENUE_GROWTH_RATE) ** year
    forecasted_ebit = forecasted_revenue * OPERATING_MARGIN
    forecasted_tax = forecasted_ebit * TAX_RATE
    forecasted_ebitda = forecasted_ebit * (1 - TAX_RATE)
    return forecasted_ebitda


def calculate_price_per_year(income_statement, year):
    forecasted_ebitda = forecast_cash_flows(income_statement, year)
    discounted_cash_flow = forecasted_ebitda / (1 + WACC) ** year
    terminal_value = discounted_cash_flow * (1 + TERMINAL_GROWTH_RATE) / (WACC - TERMINAL_GROWTH_RATE)
    present_value_terminal = terminal_value / (1 + WACC) ** FORECAST_PERIOD
    enterprise_value = discounted_cash_flow + present_value_terminal
    equity_value = enterprise_value - net_debt
    price_per_share = (equity_value / num_shares) * 1000000
    return price_per_share


# Main execution
def main() -> None:
    income_statement = load_financial_data(file_path)

    predicted_prices = []
    current_year = 2022
    for year in range(1, FORECAST_PERIOD + 1):
        price = calculate_price_per_year(income_statement, year)
        predicted_prices.append(price)

    df_predicted_prices = pd.DataFrame({
        'Year': [current_year + i for i in range(FORECAST_PERIOD)],
        'Predicted Share Price': predicted_prices
    })

    print(df_predicted_prices)
# current_year = 2022
