"""
ezfiles: Truly Simple File Operations

A beginner-friendly library that simplifies common file operations in Python.
"""

from .core import read, write, convert
from .search import find
from .metadata import info

__version__ = '0.1.0'
__all__ = ['read', 'write', 'convert', 'find', 'info']
