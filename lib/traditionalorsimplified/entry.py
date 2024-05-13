"""
This module provides functionality to determine whether a provided string is written in traditional or simplified
chinese. Results are best-guess only and will return False if result is indeterminate. Methodology here is to match
the contents of a string against a list of known differentiated characters. Most strings should only have one of
simplified characters or traditional characters. In the event that a string has both, a 'thorough' mode which makes
a determination by whichever a string contains more of, traditional or simplified characters.
"""

import os

DATA_DIR = "/".join([os.path.dirname(__file__), "data"])
TRADITIONAL_DATA_FILE = "/".join([DATA_DIR, "traditional.data"])
SIMPLIFIED_DATA_FILE = "/".join([DATA_DIR, "simplified.data"])

TRADITIONAL_DATA = None
SIMPLIFIED_DATA = None
with open(TRADITIONAL_DATA_FILE, encoding='utf-8') as data:
    TRADITIONAL_DATA = {char for char in data.read()}
with open(SIMPLIFIED_DATA_FILE, encoding='utf-8') as data:
    SIMPLIFIED_DATA = {char for char in data.read()}

def is_traditional(s: str, thorough: bool = False) -> bool:
    """Makes a determination of whether a string is written in traditional (Chinese).

    Args:
        s (str): The string to test for traditional (Chinese) characters.
        thorough (bool, optional): Setting to see if the function should scan the
            whole string for majority-voting to make a determination. Defaults to False.
    
    Returns:
        bool: True if 's' was determined to be written in traditional (Chinese). Returns False
            if the result was indeterminate
    """
    counter = 0
    for char in s:
        if char in TRADITIONAL_DATA:
            if not thorough: return True
            counter += 1
        elif char in SIMPLIFIED_DATA:
            if not thorough: return False
            counter -= 1
    return True if counter > 0 else False

def is_simplified(s: str, thorough: bool = False) -> bool:
    """Makes a determination of whether a string is written in simplified (Chinese).

    Args:
        s (str): The string to test for simplified (Chinese) characters.
        thorough (bool, optional): Setting to see if the function should scan the
            whole string for majority-voting to make a determination. Defaults to False.
    
    Returns:
        bool: True if 's' was determined to be written in simplified (Chinese). Returns False
            if the result was indeterminate.
    """
    counter = 0
    for char in s:
        if char in SIMPLIFIED_DATA:
            if not thorough: return True
            counter += 1
        elif char in TRADITIONAL_DATA:
            if not thorough: return False
            counter -= 1
    return True if counter > 0 else False