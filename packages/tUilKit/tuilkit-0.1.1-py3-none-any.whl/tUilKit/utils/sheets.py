# src/utilsbase/utils/sheets.py
"""
Contains functions for managing or working with data frames, spreadsheets, CSV, XLSX files.

"""
import pandas as pd

def read_excel(file_path):
    """
    Read an Excel file into a DataFrame.
    Args:
        file_path (str): Path to the Excel file.
    Returns:
        pd.DataFrame: DataFrame containing the Excel data.
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None

def write_excel(df, file_path, writer=None, sheet_name='Sheet1'):
    """
    Write a DataFrame to an Excel file.
    Args:
        df (pd.DataFrame): DataFrame to write.
        file_path (str): Path to the Excel file.
        writer (pd.ExcelWriter, optional): Excel writer object. If None, a new writer will be created.
        sheet_name (str): Name of the sheet to write to. Default is 'Sheet1'.
    """
    try:
        if writer is None:
            writer = pd.ExcelWriter(file_path, engine='openpyxl')
        
        df.to_excel(writer, index=False, sheet_name=sheet_name)

        if writer is None:
            writer.save()
    except Exception as e:
        print(f"Error writing Excel file: {e}")

def append_to_excel(df, file_path, sheet_name='Sheet1'):
    """
    Append data to an existing Excel file.
    Args:
        df (pd.DataFrame): DataFrame to append.
        file_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet to append to. Default is 'Sheet1'.
    """
    try:
        with pd.ExcelWriter(file_path, mode='a', engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
    except Exception as e:
        print(f"Error appending to Excel file: {e}")

def read_google_sheet(sheet_url):
    """
    Read data from a Google Sheet.
    Args:
        sheet_url (str): URL of the Google Sheet.
    Returns:
        pd.DataFrame: DataFrame containing the Google Sheet data.
    """
    try:
        csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
        df = pd.read_csv(csv_export_url)
        return df
    except Exception as e:
        print(f"Error reading Google Sheet: {e}")
        return None

def df_column(df, column='amount', operation='sum'):
    """
    Analyze wallet transactions.
    Args:
        df (pd.DataFrame): DataFrame with wallet transactions.
        operation (str): Operation to perform ('sum', 'mean', 'count'). Default is 'sum'.
        column (str): Column to perform operation on. Default is 'amount'.
    Returns:
        float or int: Result of the analysis.
    """
    if operation == 'sum':
        return df[column].sum()
    elif operation == 'mean':
        return df[column].mean()
    elif operation == 'count':
        return df[column].count()
    else:
        print(f"Unsupported operation: {operation}")
        return None
