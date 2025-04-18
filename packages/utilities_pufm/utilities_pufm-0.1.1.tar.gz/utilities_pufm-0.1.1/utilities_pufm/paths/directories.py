from rich.tree import Tree
from rich.console import Console
import os

def build_tree(path, tree):
    """
    Recursively builds a rich Tree object for the directory structure.
    
    :param path: Current directory path.
    :param tree: Rich Tree object to build upon.
    """
    for entry in os.scandir(path):
        if entry.is_dir():
            # Add directory to the tree
            branch = tree.add(f"[bold blue]{entry.name}[/]")
            # Recurse into subdirectory
            build_tree(entry.path, branch)
        else:
            # Add file to the tree
            tree.add(f"[green]{entry.name}[/]")

def print_directory_tree(root_path):
    """
    Prints the directory tree using rich.

    :param root_path: Path to the directory to visualize.
    """
    # Create the root of the tree
    tree = Tree(f"[bold magenta]{os.path.basename(root_path)}[/]")
    build_tree(root_path, tree)
    # Print the tree
    console = Console()
    console.print(tree)
    

""""
precisa verificar

"""


def create_json_directory_tree(base_path, tree_structure):
    """
    Recursively creates a directory tree.

    :param base_path: The root path where the tree will be created.
    :param tree_structure: A nested dictionary representing the directory structure.
    """
    for directory, sub_dirs in tree_structure.items():
        # Define the path for the current directory
        dir_path = os.path.join(base_path, directory)
        
        # Create the current directory
        os.makedirs(dir_path, exist_ok=True)
        
        # If there are subdirectories, create them recursively
        if isinstance(sub_dirs, dict):
            create_directory_tree(dir_path, sub_dirs)

    # Define the directory tree structure as a nested dictionary
    directory_tree = {
        "root_folder": {
            "sub_folder1": {
                "sub_sub_folder1": {},
                "sub_sub_folder2": {},
            },
            "sub_folder2": {
                "sub_sub_folder3": {},
            },
            "sub_folder3": {}
        }
    }

    # Base path where the directory tree will be created
    base_path = "my_project"

    # Generate the directory tree
    create_directory_tree(base_path, directory_tree)

    print(f"Directory tree created at: {os.path.abspath(base_path)}")
