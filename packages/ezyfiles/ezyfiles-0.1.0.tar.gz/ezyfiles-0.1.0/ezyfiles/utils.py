"""
Utility functions for the ezfiles library.
"""

import os
from pathlib import Path


def get_extension(filename):
    """
    Extract the file extension from a filename.
    
    Args:
        filename (str): Path to the file
        
    Returns:
        str: Lowercase file extension without the dot
    """
    return Path(filename).suffix.lower().lstrip('.')


def ensure_directory(path):
    """
    Create a directory if it doesn't exist.
    
    Args:
        path (str): Directory path to create
        
    Returns:
        bool: True if the directory was created or already exists
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception:
        return False