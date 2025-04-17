import subprocess
import os

from utilities_pufm.paths.paths import windows_to_wsl_path
from pathlib import Path
from utilities_pufm.prints.rich import custom_print

def remove_ignored_files(repo_path: str, mensagem: str, windows: bool = True):
    script_path = os.path.abspath(os.path.join(Path(__file__).parent, "scripts/remove_ignored_from_git.sh"))
    
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"Script file not found: {script_path}")

    command = []
    if windows:
        command.extend(["wsl", "bash"])
        script_path = windows_to_wsl_path(script_path)
        repo_path = windows_to_wsl_path(repo_path)
    
    custom_print(f"*Repo path*: {repo_path}")
    custom_print(f"*Script path*: {script_path}")
    
    command.extend([script_path, repo_path, mensagem])
    try:
        # Executa o script com os argumentos
        subprocess.run(
            command,
            check=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"❌ Error while executing the script: {e}")
