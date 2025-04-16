# ezfiles: Truly Simple File Operations

A beginner-friendly Python library that simplifies common file operations.

## Features

- **Universal Read/Write**: One function to read any file format
- **Format Conversion**: Convert between file formats with one line of code
- **Easy File Search**: Find files matching patterns without complex syntax
- **File Information**: Get file metadata quickly and easily

## Installation

```bash
pip install ezfiles
```

## Quick Start

```python
import ezfiles

# Read any file (auto-detects format)
data = ezfiles.read("myfile.csv")  # Works for .txt, .csv, .json, .xlsx, etc.

# Write data to any format
ezfiles.write(data, "output.json")  # Same function for all formats

# Convert between formats
ezfiles.convert("data.json", "data.csv")

# Find files easily
files = ezfiles.find("*.txt")  # Find all text files in current directory
more_files = ezfiles.find("*.csv", "/path/to/data", recursive=True)  # Search recursively

# Get file information
info = ezfiles.info("myfile.csv")
print(f"File size: {info['size_mb']} MB")
print(f"Last modified: {info['modified']}")
```

## Supported File Formats

- CSV files (.csv)
- Excel files (.xlsx, .xls)
- JSON files (.json)
- YAML files (.yaml, .yml)
- Text files (.txt and others)

## Requirements

- Python 3.6+
- pandas
- openpyxl
- pyyaml

## License

MIT License