# ---------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in project root for information.
# ---------------------------------------------------------------------------------

"""
file_utils.py

This module provides utility functions for reading and writing YAML and JSON files.
It is designed to simplify configuration file handling and data serialization/deserialization
in a consistent and readable format.
"""

import yaml
import json

def read_yaml(file_path):
    """
    Reads a YAML file and returns the parsed data as a Python object.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict or list: Parsed YAML content.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data

def save_yaml(data, filename):
    """
    Saves a Python object to a YAML file.

    Args:
        data (dict or list): Data to save.
        filename (str): Destination file path.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, default_flow_style=False)

def read_json(filepath):
    """
    Reads a JSON file and returns the parsed data as a Python object.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        dict or list: Parsed JSON content.
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def save_json(data, filename):
    """
    Saves a Python object to a JSON file with indentation for readability.

    Args:
        data (dict or list): Data to save.
        filename (str): Destination file path.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
