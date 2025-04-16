"""
Functions for finding files.
"""

import os
import glob
from pathlib import Path


def find(pattern, directory='.', recursive=False):
    """
    Find files matching a pattern.
    
    Args:
        pattern (str): File pattern to match (e.g., "*.csv")
        directory (str): Directory to search in (defaults to current directory)
        recursive (bool): Whether to search recursively in subdirectories
        
    Returns:
        list: List of matching file paths
        
    Examples:
        >>> csv_files = ezfiles.find("*.csv")
        >>> images = ezfiles.find("*.png", "images", recursive=True)
    """
    search_dir = Path(directory)
    
    # Ensure directory exists
    if not search_dir.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    if recursive:
        # Use ** for recursive search with glob
        if "/" in pattern or "\\" in pattern:
            # Pattern already has path components
            pattern_path = str(search_dir / pattern)
        else:
            # Add ** to search all subdirectories
            pattern_path = str(search_dir / "**" / pattern)
            
        # Return all matching files
        return [str(p) for p in Path().glob(pattern_path) if p.is_file()]
    else:
        # Simple non-recursive search
        pattern_path = str(search_dir / pattern)
        return [str(p) for p in Path().glob(pattern_path) if p.is_file()]