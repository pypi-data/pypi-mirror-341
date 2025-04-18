import sys
import os

from pathlib import Path

def add_path(new_path: str) -> None:
    """Add a new path to the system path if it is not already present.

    This function checks if the specified path is already in the system path. 
    If it is not, the function appends the new path to the system path, allowing for module imports from that location.

    Args:
        new_path (str): The path to be added to the system path.

    Returns:
        None
    """
    if new_path not in sys.path:
        sys.path.append(new_path)

def windows_to_wsl_path(windows_path):
    path = Path(windows_path).resolve()
    return f"/mnt/{path.drive[0].lower()}{str(path)[2:].replace('\\', '/')}"

def list_files_from_diretory(dir: str, endswith: str | None = None) -> list:
    """List files in a specified directory.

    This function retrieves all files from the given directory that match the specified suffix. 
    If no suffix is provided, it defaults to listing all files ending with '.json'.
    
    Args:
        dir (str): The path to the directory from which to list files.
        endswith (str | None): The suffix to filter files by. If None, all files are listed.

    Returns:
        list: A list of filenames that match the specified suffix.
    """
    return [f for f in os.listdir(dir) if f.endswith(endswith)]