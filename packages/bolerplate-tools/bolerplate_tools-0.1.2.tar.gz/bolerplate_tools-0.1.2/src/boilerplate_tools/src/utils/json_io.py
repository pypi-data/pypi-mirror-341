"""Utility functions for reading and writing JSON files."""
import json
from typing import Any, List, Dict, Union
import os


def read_json(file_path: str) -> Any:
    """
    Read a JSON file and return its contents.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Any: The parsed JSON content
        
    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file is not valid JSON
        
    Example:
        >>> data = read_json("data.json")
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(file_path: str, data: Any, indent: int = 4) -> None:
    """
    Write data to a JSON file.
    
    Args:
        file_path: Path where to write the JSON file
        data: The data to write to the file
        indent: Number of spaces for indentation (default: 4)
        
    Example:
        >>> write_json("output.json", {"name": "John", "age": 30})
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def append_json(file_path: str, items: List[Any], indent: int = 4) -> None:
    """
    Append items to a JSON list file. If the file doesn't exist or is empty,
    a new list will be created with the items.
    
    Args:
        file_path: Path to the JSON file
        items: List of items to append to the JSON file
        indent: Number of spaces for indentation (default: 4)
        
    Raises:
        TypeError: If the existing file doesn't contain a JSON list
        
    Example:
        >>> append_json("data.json", [{"name": "John"}, {"name": "Jane"}])
    """
    existing_data = []
    
    # Try to read existing file
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        existing_data = read_json(file_path)
        
        # Validate that existing data is a list
        if not isinstance(existing_data, list):
            raise TypeError(f"File {file_path} must contain a JSON list to append items")
    
    # Append new items and write back
    existing_data.extend(items)
    write_json(file_path, existing_data, indent=indent)