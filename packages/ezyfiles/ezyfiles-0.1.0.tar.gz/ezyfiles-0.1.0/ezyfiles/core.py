"""
Core functions for file reading, writing, and conversion.
"""

import os
import json
import csv
from pathlib import Path
import pandas as pd


def read(filename):
    """
    Read any supported file format automatically.
    
    Args:
        filename (str): Path to the file to read
        
    Returns:
        The contents of the file in an appropriate format:
        - CSV/Excel: pandas DataFrame
        - JSON: dict or list
        - YAML: dict or list
        - TXT: string
        
    Examples:
        >>> data = ezyfiles.read("data.csv")
        >>> config = ezyfiles.read("config.json")
    """
    # Get file extension (lowercase)
    ext = Path(filename).suffix.lower().lstrip('.')
    
    try:
        # CSV files
        if ext == 'csv':
            return pd.read_csv(filename)
        
        # Excel files
        elif ext in ['xlsx', 'xls']:
            return pd.read_excel(filename)
        
        # JSON files
        elif ext == 'json':
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # YAML files
        elif ext in ['yaml', 'yml']:
            try:
                import yaml
                with open(filename, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except ImportError:
                raise ImportError("PyYAML is required for YAML support. Install with: pip install pyyaml")
        
        # Default to text for other formats
        else:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
                
    except Exception as e:
        raise IOError(f"Error reading {filename}: {str(e)}")


def write(data, filename):
    """
    Write data to any supported file format automatically.
    
    Args:
        data: The data to write (DataFrame, dict, list, or string)
        filename (str): Path to the output file
        
    Examples:
        >>> ezyfiles.write(df, "output.csv")
        >>> ezyfiles.write(config_dict, "config.json")
    """
    # Get file extension (lowercase)
    ext = Path(filename).suffix.lower().lstrip('.')
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        # CSV files
        if ext == 'csv':
            if isinstance(data, pd.DataFrame):
                data.to_csv(filename, index=False)
            else:
                pd.DataFrame(data).to_csv(filename, index=False)
        
        # Excel files
        elif ext in ['xlsx', 'xls']:
            if isinstance(data, pd.DataFrame):
                data.to_excel(filename, index=False)
            else:
                pd.DataFrame(data).to_excel(filename, index=False)
        
        # JSON files
        elif ext == 'json':
            if isinstance(data, pd.DataFrame):
                data = data.to_dict(orient='records')
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        
        # YAML files
        elif ext in ['yaml', 'yml']:
            try:
                import yaml
                
                if isinstance(data, pd.DataFrame):
                    data = data.to_dict(orient='records')
                
                with open(filename, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False)
            except ImportError:
                raise ImportError("PyYAML is required for YAML support. Install with: pip install pyyaml")
        
        # Default to text for other formats
        else:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(data))
                
    except Exception as e:
        raise IOError(f"Error writing to {filename}: {str(e)}")


def convert(source_file, target_file):
    """
    Convert a file from one format to another.
    
    Args:
        source_file (str): Path to the source file
        target_file (str): Path to the output file
        
    Examples:
        >>> ezyfiles.convert("data.json", "data.csv")
        >>> ezyfiles.convert("config.yaml", "config.json")
    """
    # Read the source file
    data = read(source_file)
    
    # Write to the target file
    write(data, target_file)
    
    return f"Converted {source_file} to {target_file}"