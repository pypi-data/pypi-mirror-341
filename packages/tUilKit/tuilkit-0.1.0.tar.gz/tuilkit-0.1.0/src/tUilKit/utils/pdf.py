# src/utilsbase/utils/pdf.py
"""
Contains functions for managing or working with PDF files.

"""
import PyPDF2

""" UNVERIFIED OR NOT TESTED FUNCTION 
        Search for specific string within a PDF file
Description: Opens the PDF file, reads its content, and searches for the specified strings.
Argument:   - file_path (str): The path to the PDF file.
Argument:   - search_str (list): A list of strings to search for.
Return value: True if any of the search strings are found in the PDF file, otherwise False."""
def search_pdf(file_path, search_str):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            text = reader.pages[page_num].extract_text()
            for term in search_str:
                if term in text:
                    return True
    return False
