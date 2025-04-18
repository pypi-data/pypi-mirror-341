import json

import numpy as np
import pandas as pd

from datetime import datetime, date
from decimal import Decimal
from uuid import UUID
from typing import Dict

def load_json(json_path: str) -> object:
    """Load data from a JSON file.

    This function reads a JSON file from the specified path and returns the data as a Python object. 
    It handles errors related to file not found and invalid JSON format, providing informative messages.

    Args:
        json_path (str): The path to the JSON file to be loaded.

    Returns:
        Any: The data loaded from the JSON file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file does not contain valid JSON.
    """

    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Erro: O arquivo '{json_path}' não foi encontrado.")
        raise
    except json.JSONDecodeError as e:
        print(f"Erro: O arquivo '{json_path}' não contém um JSON válido.\n{e}")
        raise

def load_or_create_json(json_path: str, data: dict = {}) -> Dict:
    """Load data from a JSON file or create a new file if it doesn't exist.

    This function attempts to load data from an existing JSON file at the specified path. 
    If the file does not exist, it creates a new empty file and returns an empty dictionary.
    It handles errors related to file not found and invalid JSON format, providing informative messages.

    Args:
        json_path (str): The path to the JSON file to be loaded or created.

    Returns:
        Any: The data loaded from the JSON file or an empty dictionary if the file doesn't exist.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file does not contain valid JSON.
    """

    try:    
        return load_json(json_path)
    except FileNotFoundError:
        save_json(json_path, data)
        return data   
    except json.JSONDecodeError as e:
        print(f"Erro: O arquivo '{json_path}' não contém um JSON válido.\n{e}")
        raise

def save_json(file_path, data):
    """Save data to a JSON file.

    This function writes the provided data to a specified file in JSON format. 
    The data is formatted with an indentation of four spaces for better readability.

    Args:
        file_path (str): The path to the file where the JSON data will be saved.
        data (Any): The data to be saved in JSON format.

    Returns:
        None
    """

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

def make_obj_json_serializable(obj):

    def handle_dict(dict):
        return {key: make_obj_json_serializable(value) for key, value in dict.items()}
    
    # Handle None
    if obj is None:
        # print("[JSON WARNING]: Object is None.")
        return None
        
    # Handle basic types that are already serializable
    if isinstance(obj, (bool, int, float, str)):
        # print("[JSON WARNING]: Object is already serializable.")
        return obj
    
    # Handle numpy numeric types
    if isinstance(obj, (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)):
        return int(obj)
    
    if isinstance(obj, (np.float16, np.float32, np.float64)):
        return float(obj)
    
    # Handle numpy arrays
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    
    # Handle datetime objects
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    
    # Handle Decimal
    if isinstance(obj, Decimal):
        return str(obj)
    
    # Handle UUID
    if isinstance(obj, UUID):
        return str(obj)
    
    # Handle pandas Series/DataFrame
    if isinstance(obj, (pd.Series, pd.DataFrame)):
        return handle_dict(obj.to_dict())
        
    # Handle dictionaries recursively
    if isinstance(obj, dict):
        return handle_dict(obj)
        
    # Handle iterables (lists, tuples, sets)
    if isinstance(obj, (list, tuple, set)):
        return [make_obj_json_serializable(item) for item in obj]
    
    # Handle any other objects by converting to string
    try:
        return str(obj)
    except Exception:
        return f"<non-serializable: {type(obj).__name__}>"
    