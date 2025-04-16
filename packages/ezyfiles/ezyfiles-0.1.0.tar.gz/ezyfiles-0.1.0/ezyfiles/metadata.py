"""
Functions for retrieving file metadata.
"""

import os
import datetime
from pathlib import Path


def info(filename):
    """
    Get basic information about a file.
    
    Args:
        filename (str): Path to the file
        
    Returns:
        dict: Dictionary containing file information
        
    Examples:
        >>> file_info = ezfiles.info("data.csv")
        >>> print(f"Size: {file_info['size_mb']} MB")
    """
    file_path = Path(filename)
    
    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {filename}")
    
    # Get file stats
    stats = file_path.stat()
    
    # Format creation and modification times
    creation_time = datetime.datetime.fromtimestamp(stats.st_ctime)
    modified_time = datetime.datetime.fromtimestamp(stats.st_mtime)
    
    # Get file extension
    extension = file_path.suffix.lower().lstrip('.')
    
    # Calculate file size in different units
    size_bytes = stats.st_size
    size_kb = size_bytes / 1024
    size_mb = size_kb / 1024
    
    # Return dictionary with file information
    return {
        'name': file_path.name,
        'path': str(file_path.absolute()),
        'extension': extension,
        'size_bytes': size_bytes,
        'size_kb': round(size_kb, 2),
        'size_mb': round(size_mb, 2),
        'created': creation_time,
        'modified': modified_time,
        'is_file': file_path.is_file(),
        'is_directory': file_path.is_dir(),
    }