# src/utilsbase/utils/calc.py

import pandas as pd
from utils.output import colour_log, log_done, log_exception, log_message, colour_fstr
from utils.data import read_historical_data, get_historical_price

def calculate_units(df):
    """Add the 'Units' column to the DataFrame."""
    # df['Units'] = df.apply(lambda row: row['Units_Received'] if row['Action'] in ['Buy', 'Reward', 'Receive', 'Other'] else -row['Units_Sent'], axis=1)
    df['Units'] = df.apply(lambda row: -row['Units_Sent'] if row['Action'] in ['Send', 'Sell', 'Withdrawal'] else row['Units_Received'], axis=1)

def calculate_acb_and_gains(df):
    """Calculate Adjusted Cost Basis (ACB) and Realized Gains/Losses."""
    # Initialize variables for ACB and transactions
    acb, total_units, total_realized_gains, total_distributions, total_cashback = {}, {}, {}, {}, {}
    acb_list, total_qty_list, acb_per_unit_list, gain_loss_list = [], [], [], []
    sell_transactions, distribution_transactions, cashback_transactions = [], [], []
    gain_loss_value = 0
    for index, row in df.iterrows():
        currency = row['Currency_Sent'] if row['Units'] < 0 else row['Currency_Received']
        if pd.isna(currency) or currency == "":
            continue  # Skip invalid currencies

        if currency not in acb:
            acb[currency] = 0
            total_units[currency] = 0
            total_realized_gains[currency] = 0
            total_distributions[currency] = 0
            total_cashback[currency] = 0

        # Handle sell/send transactions
        if row['Units'] < 0:
            lot_size = -row['Units']
            acb_per_unit = acb[currency] / total_units[currency] if total_units[currency] != 0 else 0
            gain_loss_value = row['Book_Cost'] - lot_size * acb_per_unit
            
            acb[currency] -= lot_size * acb_per_unit
            acb[currency] = max(acb[currency], 0)  # Ensure ACB doesn't go negative
            total_units[currency] -= lot_size
            total_realized_gains[currency] += gain_loss_value

            sell_transactions.append({
                'Date': row['Date'],
                'Currency': currency,
                'ACB/Unit': acb_per_unit,
                'Qty Sold': lot_size,
                'Realized Profit/Loss': gain_loss_value,
                'Description': row['Description']  # Include the description
            })

        # Handle buy/receive/reward/other transactions
        elif row['Units'] > 0:
            gain_loss_value = None
            lot_size = row['Units']
            acb[currency] += row['Book_Cost']
            total_units[currency] += lot_size

            # Check for 'Reward' and 'Other' transactions
            if row['Action'] in ['Reward', 'Other']:
                if row['Description'] in ['Bitcoin cashback', 'ShakeSquad']:
                    # Add to the 'Cashback' category
                    if 'total_cashback' not in locals():
                        total_cashback = {}  # Initialize the variable if it doesn't exist
                    if currency not in total_cashback:
                        total_cashback[currency] = 0  # Initialize for the currency
                    total_cashback[currency] += row['Book_Cost']
                    cashback_transactions.append({
                        'Date': row['Date'],
                        'Currency': currency,
                        'Action': row['Action'],
                        'Units Received': row['Units_Received'],
                        'Book Cost': row['Book_Cost'],
                        'Description': row['Description']  # Include the description
                    })
                else:
                    # Add to Distributions category
                    total_distributions[currency] += row['Book_Cost']
                    distribution_transactions.append({
                        'Date': row['Date'],
                        'Currency': currency,
                        'Action': row['Action'],
                        'Units Received': row['Units_Received'],
                        'Book Cost': row['Book_Cost'],
                        'Description': row['Description']  # Include the description
                    })
        acb_list.append(acb[currency])
        total_qty_list.append(total_units[currency])
        acb_per_unit_list.append(acb[currency] / total_units[currency] if total_units[currency] > 0 else 0)
        gain_loss_list.append(None if row['Units'] >= 0 else gain_loss_value)
    df['ACB'] = acb_list
    df['Total Units'] = total_qty_list
    df['Gain/Loss'] = gain_loss_list
    df['ACB/Unit'] = acb_per_unit_list

    return df, sell_transactions, distribution_transactions, cashback_transactions, total_realized_gains, total_distributions, total_cashback

def newton_logic(df):
    """Convert Newton transaction history to the required format."""
    # Rename columns to match the expected headers
    df.rename(columns={
        'Type': 'Action',
        'Received Quantity': 'Units_Received',
        'Received Currency': 'Currency_Received',
        'Sent Quantity': 'Units_Sent',
        'Sent Currency': 'Currency_Sent',
        'Tag': 'Description'
    }, inplace=True)

    # Convert 'Date' column to datetime, coercing errors
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])  # Drop rows where 'Date' couldn't be parsed
    df = df.sort_values(by='Date')

    # Add 'Book_Cost' column initialized with None or 0
    df['Book_Cost'] = 0

    # Convert TRADE type actions into BUY or SELL transactions
    df['Action'] = df.apply(lambda row: 'Buy' if row['Action'] == 'TRADE' and row['Currency_Received'] != 'CAD' else ('Sell' if row['Action'] == 'TRADE' and row['Currency_Received'] == 'CAD' else row['Action']), axis=1)
    df['Units'] = df.apply(lambda row: row['Units_Received'] if row['Action'] in ['Buy','Deposit','DEPOSIT'] else (-row['Units_Sent'] if row['Action'] == 'Sell' else row['Units_Received']), axis=1)
    
    for index, row in df.iterrows():
        currency = row['Currency_Received']
        transaction_date = row['Date']
        if row['Description'] == "Referral Program":     
            # This is actually a Reward Transaction
            df.loc[index, 'Action'] = 'Reward'
            df.loc[index, 'Book_Cost'] = float(row['Units_Received'])
            log_message(colour_fstr("Reward: $", "OUTPUT", f"{df.loc[index, 'Book_Cost']:.2f} ", "INFO", f"in {currency} ", "ARGS", "Referral Program"))
        elif row['Action'] == 'REWARD' and row['Currency_Received'] != 'CAD':
            # These Staking Reward transactions are in a different currency
            historical_folder = f'historical/{currency}_CAD'
            historical_price = get_historical_price(currency, transaction_date, historical_folder)
            df.loc[index, 'Action'] = 'Reward'
            df.loc[index, 'Book_Cost'] = row['Units_Received'] * historical_price
            log_message(colour_fstr("Stake: $", "OUTPUT", f"{df.loc[index, 'Book_Cost']:.2f} ", "INFO", f"in {currency} "), end="")
        elif row['Action'] == 'DEPOSIT' and row['Currency_Received'] != 'CAD':
            # This is actually a Receive Transaction
            historical_folder = f'historical/{currency}_CAD'
            historical_price = get_historical_price(currency, transaction_date, historical_folder)
            df.loc[index, 'Book_Cost'] = float(row['Units_Received']) * historical_price
            df.loc[index, 'Action'] = 'Receive'
            colour_log("Receive Transaction on: ", "DATE", transaction_date, " ", "OUTPUT", f"${df.loc[index, 'Book_Cost']:.2f}")
        elif row['Action'] == 'DEPOSIT' and row['Currency_Received'] == 'CAD':
            # Deposit Transaction in CAD cash
            df.loc[index, 'Action'] = 'Deposit'
            df.loc[index, 'Book_Cost'] = float(row['Units_Received'])
            colour_log("CAD Deposit Transaction on: ", "DATE", transaction_date, " ", "OUTPUT", f"${df.loc[index, 'Book_Cost']:.2f}")
        elif row['Action'] == 'WITHDRAWN' and row['Currency_Sent'] == 'CAD':
            # Withdrawal Transaciton in CAD cash
            df.loc[index, 'Action'] = 'Withdrawal'
            df.loc[index, 'Book_Cost'] = float(row['Units_Sent'])
            currency = row['Currency_Sent']
            colour_log("CAD Withdrawal Transaction on: ", "DATE", transaction_date, " ", "OUTPUT", f"${df.loc[index, 'Book_Cost']:.2f}")
        # elif row['Action'] == 'SEND':
        #     # Skip SEND transactions
        #     continue
        # elif row['Action'] == 'RECEIVE':
        #     # Skip RECEIVE transactions
        #     continue
        # elif row['Action'] == 'Buy':            
        #     # Buy Transaction
        #     df.loc[index, 'Book_Cost'] = float(row['Units_Sent'])
        #     continue
        # elif row['Action'] == 'Sell':
        #     # Sell Transaction
        #     df.loc[index, 'Book_Cost'] = float(row['Units_Received'])
        #     continue
        else:
            df.loc[index, 'Book_Cost'] = 0
    return df

def generate_summary(df, total_realized_gains, total_distributions, total_cashback):
    """Generate the summary DataFrame."""
    all_currencies = pd.concat([df['Currency_Received'], df['Currency_Sent']]).dropna().unique()
    summary_data = {'Currency': [], 'ACB': [], 'Realized Gain/Loss': [], 'Distributions': [], 'Cashback': []}

    for currency in all_currencies:
        currency_df = df[(df['Currency_Received'] == currency) | (df['Currency_Sent'] == currency)]
        acb_final = currency_df['ACB'].dropna().iloc[-1] if not currency_df['ACB'].dropna().empty else 0
        gain_loss_total = total_realized_gains.get(currency, 0)
        distribution = total_distributions.get(currency, 0)
        cashback = total_cashback.get(currency, 0)
        if currency.strip() != "":  # Exclude blank currencies
            summary_data['Currency'].append(currency)
            summary_data['ACB'].append(acb_final)
            summary_data['Realized Gain/Loss'].append(gain_loss_total)
            summary_data['Distributions'].append(distribution)
            summary_data['Cashback'].append(cashback)

    return pd.DataFrame(summary_data)

def match_and_adjust_acb_combined(df, tolerance=0.0001, date_tolerance=1):
    """
    Match send and receive transactions and adjust ACB on the receive side.
    Args:
        df (pd.DataFrame): Combined wallet DataFrame.
        tolerance (float): Tolerance for amount matching.
        date_tolerance (int): Tolerance for date matching (in days).
    Returns:
        pd.DataFrame: Updated combined DataFrame with adjusted ACB.
        pd.DataFrame: Unmatched transactions.
        pd.DataFrame: Matched transactions.
    """
    matches = []
    unmatched_df = df.copy()

    for index_send, row_send in df[df['Action'] == 'Send'].iterrows():
        for index_receive, row_receive in df[df['Action'] == 'Receive'].iterrows():
            if (
                row_send['Currency_Sent'] == row_receive['Currency_Received'] and
                abs(row_send['Units_Sent'] - row_receive['Units_Received']) <= tolerance and
                row_receive['Date'] > row_send['Date'] and  # Ensure receive happens after send
                abs((row_send['Date'] - row_receive['Date']).days) <= date_tolerance
            ):
                # Send/Receive Match Logic Goes Here.  Calculations are run before & after to set up & initialize important columns
                # Second run through of calculations after these adjustments to ACB are made.
                transaction_date = row_receive['Date']
                currency = row_receive['Currency_Received']
                historical_folder = f'historical/{currency}_CAD'
                historical_price = get_historical_price(currency, transaction_date, historical_folder)
                acb_adjustment = row_send['Gain/Loss']
                
                colour_log("Send/Receive Match Produced At: ","DATE",transaction_date, " Spot Rate: $", "OUTPUT", f"{historical_price:.2f} ", "DATA", "ACB Adjustment: ", "OUTPUT", f"{acb_adjustment:6.2f} ")                

                adjusted_acb = row_send['Book_Cost'] - acb_adjustment

                df.at[index_send, 'Book_Cost'] = adjusted_acb
                df.at[index_send, 'Gain/Loss'] = None
                df.at[index_receive, 'Book_Cost'] = adjusted_acb
                df.at[index_receive, 'ACB'] = adjusted_acb
                df.at[index_receive, 'Spot Rate'] = historical_price

                matches.append({
                    'Send Index': index_send,
                    'Receive Index': index_receive,
                    'Date Send': row_send['Date'],
                    'Date Receive': row_receive['Date'],
                    'Currency': row_send['Currency_Sent'],
                    'Amount Sent': row_send['Units_Sent'],
                    'Amount Received': row_receive['Units_Received'],
                    'Adjusted ACB': adjusted_acb
                })

                unmatched_df = unmatched_df.drop(index_send)
                unmatched_df = unmatched_df.drop(index_receive)
                break

    matches_df = pd.DataFrame(matches)
    return df, unmatched_df, matches_df
