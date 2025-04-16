# src/py-tuilkit/config/config.py
"""
    Load JSON configuration of GLOBAL variables.
"""
import os
import json

# Define the path to the JSON file
def get_json_path(file):
    return os.path.join(os.path.dirname(__file__), file)

# Load the configuration
def load_config(json_file_path):
    with open(json_file_path, 'r') as f:
        return json.load(f)

# Initialize configurations
global_config = load_config(get_json_path('GLOBAL_CONFIG.json'))
column_mapping = load_config(get_json_path('COLUMN_MAPPING.json'))
LOG_FILE = f"{global_config['FOLDER_PATHS']['LOG_FILES']}{global_config['FILES']['LOG_FILE']}"
TEST_LOGS_FOLDER = f"{global_config['FOLDER_PATHS']['TEST_LOG_FILES']}"
