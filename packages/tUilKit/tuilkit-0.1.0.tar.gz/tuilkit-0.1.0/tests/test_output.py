# tUilKit\tests\test_output.py
"""
This module contains test functions to verify the soundness of output functions 
from the py_tuilkit.utils.output module.
"""

import sys
import os
import pandas as pd

# Ensure the base directory of the project is included in the system path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\src'))
print(f"Base Directory: {base_dir}")

if os.path.exists(base_dir):
    print(f"{base_dir} exists!")
else:
    print(f"{base_dir} does not exist. Please check your directory structure.")

if base_dir not in sys.path:
    sys.path.insert(0, base_dir)
    print("Added base directory to sys.path")

try:
    from tUilKit.config.config import TEST_LOGS_FOLDER, load_config, get_json_path # type: ignore
    print("Imported successfully!")
except ImportError as e:
    print(f"ImportError: {e}")