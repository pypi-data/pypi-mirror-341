# src/utilsbase/utils/wallet.py
"""
Contains functions for managing or working with crypto transaction histories.

# """

import pandas as pd
import os
from utils.output import colour_log, log_exception

def load_wallet(file_path):
    try:
        df = pd.read_excel(file_path)
        colour_log("DONE","Successfully ", "LOAD", "Loaded ","INFO", "wallet data from ", "PATH", os.path.dirname(file_path), "/", "FILE", os.path.basename(file_path))
        return df
    except PermissionError:
        colour_log("FILE", os.path.basename(file_path), " ", "TEXT", " is already open.  ", "COMMAND", "Skipping file.")
        return None
    except Exception as e:
        log_exception("Unable to load wallet data: ", e)
        return None

def save_wallet(df, file_path):
    try:
        df.to_excel(file_path, index=False)
        colour_log("SAVE", "Saved ","INFO", "wallet data to ", "PATH", os.path.dirname(file_path), "/", "FILE", os.path.basename(file_path))
    except Exception as e:
        log_exception("Unable to save wallet data: ", e)

def convert_wallet(df, column_mapping):
    try:
        colour_log("FILE", df.name if hasattr(df, 'name') else "DataFrame ","Existing Column List: ", "LIST", list(df.columns))

        # Iterate through matched columns and log each one
        colour_log("LIST", "List ", "INFO", "of Column Revisions:")
        matched_columns = {col: column_mapping[col] for col in df.columns if col in column_mapping}
        for col in matched_columns:
            colour_log("LIST", "Column ", "DATA", col, "LIST", " --> ", "OUTPUT", matched_columns[col])

        df.rename(columns=column_mapping, inplace=True)
        colour_log("Final Column List: ", "LIST", list(df.columns))
        colour_log("Renamed column headers based on mapping")

        return df
    except Exception as e:
        log_exception("Unable to convert wallet data columns: ", e)
        return df
    
