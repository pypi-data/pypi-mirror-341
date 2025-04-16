# src/utilsbase/utils/data.py

import pandas as pd
import os

def read_historical_data(folder_path, currency_name):
    # List all files in the folder
    files = os.listdir(folder_path)
    
    # Filter files that start with the currency name
    currency_files = [file for file in files if file.startswith(currency_name)]
    
    # Read each file into a DataFrame and concatenate them
    data_frames = []
    for file in currency_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_excel(file_path)
        data_frames.append(df)
    
    # Concatenate all DataFrames into one
    historical_data = pd.concat(data_frames, ignore_index=True)
    
    return historical_data

def get_historical_price(currency, date, folder_path):
    # Read historical data for the currency
    historical_data = read_historical_data(folder_path, currency)
    
    # Find the closest price for the given date
    historical_data['Date'] = pd.to_datetime(historical_data['Date'])
    closest_row = historical_data.iloc[(historical_data['Date'] - date).abs().argsort()[:1]]
    historical_price = closest_row['Price'].values[0]
    
    return historical_price