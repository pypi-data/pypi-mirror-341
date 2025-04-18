import os

def update_file(file_path: str, content: str) -> None:
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(content)
        
def save_file(file_path: str, content: str, how: str = "w") -> None:
    
    directory = os.path.dirname(file_path)
    
    create_dir_if_not_exist(dir_path=directory)
        
    with open(file_path, how, encoding="utf-8") as f:
        f.write(content)
        
def create_dir_if_not_exist(dir_path: str) -> None:
    if dir_path and (not os.path.exists(dir_path)):
        os.makedirs(dir_path, exist_ok=True)