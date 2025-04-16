# py-tuilkit\tests\test_module.py
"""
This module contains test functions to verify the soundness of output functions 
from the utilsbase.utils.output module.
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
    
try:
    print (f"Attempting Import of : {base_dir}\\tUilKit\\dict\\DICT_COLOURS.py", end="")
    from tUilKit.dict.DICT_COLOURS import RGB
    print ("...DONE!")
except ImportError as e:
    raise ImportError(f"Failed to import from {base_dir}\\tUilKit\\dict\\DICT_COLOURS.py: {e}")

try:
    print (f"Attempting Import of : {base_dir}\\tUilKit\\dict\\DICT_CODES.py", end="")
    from tUilKit.dict.DICT_CODES import ESCAPES, COMMANDS
    print ("...DONE!")
except ImportError as e:
    raise ImportError(f"Failed to import from {base_dir}\\tUilKit\\dict\\DICT_CODES.py: {e}")

try:
    print (f"Attempting Import of : {base_dir}\\tUilKit\\utils\\output.py", end="")
    from tUilKit.utils.output import (
        get_fg_colour,
        strip_ansi,
        append_time,
        split_time_string,
        log_message,
        colour_fstr,
        colour_log,
        log_exception,
        log_column_list,
        log_done,
        print_rainbow_row, 
        print_top_border,
        print_bottom_border,
        apply_border,
        print_text_line,
        SET_FG_COLOUR,
        SET_BG_COLOUR,
        ANSI_RESET,
        ANSI_FG_COLOUR_SET
    )
    print ("...DONE!")
except ImportError as e:
    raise ImportError(f"Failed to import from {base_dir}\\utilsbase\\utils\\output.py: {e}")

try:
    print (f"Attempting Import of : {base_dir}\\utilsbase\\utils\\fs.py", end="")
    from tUilKit.utils.fs import (
        validate_and_create_folder,
        no_overwrite
    )
    print ("...DONE!")
except ImportError as e:
    raise ImportError(f"Failed to import from {base_dir}\\utilsbase\\utils\\fs.py: {e}")


"""
Function to retrieve the custom colour code from the COLOURS.json file
RGB Hex values are hardcoded in the dict.DICT_COLOURS module in the RGB dictionary 
and converted to ANSI escape codes in the utils.output module.
"""
def test_colour_fstr(log_file=None):
    message = colour_fstr("INFO", "Coloured", "ARGS", "String:", "DATA", "Hello,", "OUTPUT", "World!")
    log_message(message, log_file=log_file)

def test_strip_ansi(log_file=None):
    # Hardcoded ANSI sequence
    coloured_string = "\033[92mThis should be green text\033[0m and this should be default coloured."
    stripped_string = strip_ansi(coloured_string)    
    log_message(f"Original String (Hardcoded): {coloured_string}", log_file=log_file)
    log_message(f"Stripped String (Hardcoded): {stripped_string}", log_file=log_file)
    
    # Dynamically generated ANSI sequence
    string_var = f"{get_fg_colour("OUTPUT")}Output Text{ANSI_RESET}"
    stripped_string_var = strip_ansi(string_var)
    log_message(f"Original String (Variable): {string_var}", log_file=log_file)
    log_message(f"Stripped String (Variable): {stripped_string_var}", log_file=log_file)
    
    # Experimentally generate a different dynamically generated ANSI sequence
    config = load_config(get_json_path("COLOURS.json"))
    new_sequence = config["COLOUR_KEY"]
    colour = new_sequence["ARGS"]
    colour_code = SET_FG_COLOUR + RGB[colour]
    dynamic_string_var = f"{ANSI_RESET}This should be in {colour_code}args{ANSI_RESET} colour text"
    dynamic_stripped_string_var = strip_ansi(dynamic_string_var)
    log_message(f"Original String (Experimental): {dynamic_string_var}", log_file=log_file)
    log_message(f"Stripped String (Experimental): {dynamic_stripped_string_var}", log_file=log_file)

    assert stripped_string in "This should be green text and this should be default coloured.", \
        f"Expected %[{stripped_string}]% in stripped string, but got %[{stripped_string}]%"
    assert stripped_string_var in "Output Text", \
        f"Expected %[{stripped_string_var}]% in stripped string, but got %[{stripped_string_var}]%"
    assert dynamic_stripped_string_var in "This should be in args colour text", \
        f"Expected %[{dynamic_stripped_string_var}]% in stripped string, but got %[{dynamic_stripped_string_var}]%"
    colour_log("PROC","test_strip_ansi","DONE","passed!", log_file=log_file) 

def test_get_fg_colour(log_file=None):
    config = load_config(get_json_path("COLOURS.json")) 
    KEY_SET = config['COLOUR_KEY']
    total_keys = len(KEY_SET)
    message = colour_fstr("INFO", "Total number of keys in COLOUR_KEY: ", "DATA", f"{total_keys}")
    log_message(message, log_file=log_file)

    keys_to_log = list(KEY_SET.keys())[:10]
    for key in keys_to_log:
        colour_code = get_fg_colour(key)
        log_message(f"Colour code for {colour_code}{key}: {KEY_SET[key]}{ANSI_RESET}", log_file=log_file)
    
    if total_keys > 10 and log_file:
        print(f"Only the first 10 keys are displayed on the screen. The remainder of the dictionary is logged in the log file if logging active.")
        for key in list(KEY_SET.keys())[10:]:
            colour_code = get_fg_colour(key)
            with open(log_file, 'a') as log:
                log.write(f"Colour code for {colour_code}{key}: {KEY_SET[key]}{ANSI_RESET}")

def test_append_time(log_file=None):
    log_message(colour_fstr("INFO","Time String:","TIME",f"%{append_time()}%"), log_file=log_file)
    if log_file:
        with open(log_file, 'r') as log:
            logged_message = log.read().strip()
        assert "Time String:" in logged_message, f"Expected 'Time String:' in logged message, but got %[{logged_message}]%"
    colour_log("PROC","test_append_time","DONE","passed!", log_file=log_file) 

def test_split_time_string(log_file=None):
    date,time = split_time_string(append_time())
    datestop = f"{date}."
    timestop = f"{time}."
    log_message(colour_fstr("The Date is","DATE", datestop, "INFO", "The Time is", "TIME", timestop, "INFO"), log_file=log_file)
    if log_file:
        with open(log_file, 'r') as log:
            logged_message = log.read().strip()
        assert date in logged_message and time in logged_message, f"Expected %[{date}]% and %[{time}]% in logged message, but got %[{logged_message}]%"
    colour_log("PROC","test_split_time_string","DONE","passed!", log_file=log_file)

def test_log_message(log_file=None):
    test_message = "This is a test log message."
    log_message(test_message, log_file=log_file)
    if log_file:
        with open(log_file, 'r') as log:
            logged_message = log.read().strip()
        assert test_message in logged_message, f"Expected %[{test_message}]% in logged message, but got %[{logged_message}]%"
    colour_log("PROC","test_log_message","DONE","passed!", log_file=log_file)

def test_colour_log(log_file=None):
    test_message = ["RED","This is red,","GREEN","and this is green,","YELLOW","and this is yellow,","DATA","and this is data"]
    message = colour_fstr(*test_message)
    message_text = strip_ansi(message)
    colour_log(message, log_file=log_file)
    if log_file:
        with open(log_file, 'r') as log:
            logged_message = log.read().strip()
        assert message_text in logged_message, f"Expected %[{test_message}]% in logged message, but got %[{logged_message}]%"
    colour_log("PROC","test_colour_log", "DONE", "passed!", log_file=log_file)

def test_log_exception(log_file=None):
    description = "Test exception logging"
    try:
        raise ValueError("This is a test exception")
    except ValueError as e:
        log_exception(description, e, log_file=log_file)
        if log_file:
            with open(log_file, 'r') as log:
                logged_message = log.readlines()
            # Check for a date and time string at the start of the line
            for line in logged_message:
                if line.strip():  # Skip empty lines
                    if line.startswith("2025"):                        
                        assert "UNEXPECTED ERROR: Test exception logging This is a test exception" in line, \
                            f"Expected exception details in logged message, but got %[{line}]%"                
        colour_log("PROC","test_log_exception","DONE", "passed!", log_file=log_file)

def test_log_column_list(log_file=None):
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    filename = "test_file.csv"
    log_column_list(df, filename, log_file=log_file)
    if log_file:
        with open(log_file, 'r') as log:
            logged_message = log.read()
        assert "Columns" in logged_message and "A" in logged_message and "B" in logged_message, \
            f"Expected column names in logged message, but got %[{logged_message}]%"
    colour_log("PROC","test_log_column_list","DONE", "passed!", log_file=log_file)

def test_log_done(log_file=None):
    log_done(log_file=log_file)
    if log_file:
        with open(log_file, 'r') as log:
            logged_message = log.read().strip()
        assert "Done!" in logged_message, f"Expected 'Done!' in logged message, but got %[{logged_message}]%"
    colour_log("PROC","test_log_done","DONE", "passed!", log_file=log_file)
    

def test_print_rainbow_row(log_file=None):
    print_rainbow_row(pattern="X-O-", spacer=2, log_file=log_file)
    if log_file:
        with open(log_file, 'r') as log:
            logged_message = log.read()
        assert "X-O-" in logged_message, f"Expected pattern 'X-O-' in logged message, but got %[{logged_message}]%"
        colour_log("PROC","test_print_rainbow_row","DONE", "passed!", log_file=log_file)

def test_apply_border(log_file=None):
    pattern = {
        "TOP": ["*"],
        "LEFT": ["|"],
        "RIGHT": ["|"],
        "BOTTOM": ["*"]
    }
    text = "Test Border"
    apply_border(text, pattern, total_length=20, index=0, log_file=log_file, text_colour="WINE", border_colour="BURGUNDY")
    colour_log("PROC","test_apply_border","DONE", "passed!", log_file=log_file)

if __name__ == "__main__":
    # Define a border pattern
    border_pattern = {
        "TOP": ["*"],
        "LEFT": ["|"],
        "RIGHT": ["|"],
        "BOTTOM": ["*"]
    }

    # Helper function to print a bordered title
    def print_test_title(title, log_file=None, border_colour="INFO", text_colour="INFO"):
        test_title=f"Running Test Function {title}"
        apply_border(test_title, border_pattern, total_length=50, index=0, log_file=log_file, border_colour=border_colour, text_colour=text_colour)

    validate_and_create_folder(TEST_LOGS_FOLDER, log_file=None)

    # List of test functions and their corresponding log files
    test_set = [
        ("RED", "RED", "test_get_fg_colour", "testlog.get_fg_colour.txt"),                  # Successfully tested
        ("ORANGE", "ORANGE", "test_colour_fstr", "testlog.colour_fstr.txt"),                # Successfully tested
        ("YELLOW", "YELLOW", "test_strip_ansi", "testlog.strip_ansi.txt"),                  # Successfully tested
        ("GREEN", "GREEN", "test_append_time", "testlog.append_time.txt"),                  # Successfully tested
        ("CYAN", "CYAN", "test_split_time_string", "testlog.split_time_string.txt"),        # Successfully tested
        ("BLUE", "BLUE", "test_colour_log", "testlog.colour_log.txt"),                      # Successfully tested
        ("MAGENTA", "MAGENTA", "test_print_rainbow_row", "testlog.rainbow_row.txt"),        # Successfully tested    
        ("PURPLE", "PURPLE", "test_apply_border", "testlog.apply_border.txt"),              # Successfully tested
        ("PURPLE", "PURPLE", "test_log_message", "testlog.log_message.txt"),                # Successfully tested
        ("PURPLE", "PURPLE", "test_log_exception", "testlog.log_exception.txt"),            # Successfully tested
        ("PURPLE", "PURPLE", "test_log_done", "testlog.log_done.txt"),                      # Successfully tested
        ("PURPLE", "PURPLE", "test_log_column_list", "testlog.log_column_list.txt") # ,     # Successfully tested
    ]

    # Run tests with rainbow row and bordered titles
    for text_colour, border_colour, test_name, log_file in test_set:
        log_file_path = f"{TEST_LOGS_FOLDER}{log_file}"
        print_rainbow_row(pattern="X-O-", spacer=2, log_file=log_file_path)
        print_test_title(test_name, log_file=log_file_path, border_colour=border_colour, text_colour=text_colour)
        try:
            globals()[test_name](log_file=log_file_path)
        except Exception as e:
            log_message(f"{test_name} failed: {e}", log_file=log_file_path)

    print_rainbow_row(pattern="<-O->", spacer=2, log_file=log_file_path)
    print_test_title("All Tests Complete", log_file=log_file_path, border_colour="MAROON", text_colour="PINK")
    print_rainbow_row(pattern="<-O->", spacer=2, log_file=log_file_path)