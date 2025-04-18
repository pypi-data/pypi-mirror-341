import subprocess

from utilities_pufm.prints.rich import custom_print

class GitManager:
    _instance = None
    updated = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GitManager, cls).__new__(cls)
            cls._instance._initialized = False

        return cls._instance
    
    def __init__(self) -> None:
        
        if not self.updated:
            self.pull_done()
    
    def pull_done(self):
        try:
            status_output = subprocess.check_output(['git', 'status', '-uno'], text=True)
            
            if "Your branch is behind" in status_output:
                custom_print("*[YOUR BRANCH IS BEHIND*]: Executing 'git pull'", rich=True)
                subprocess.run(['git', 'pull'])
                custom_print("*[YOUR BRANCH IS UPDATED]*: Repostory updated.", rich=True)
                self.updated = True
            else:
                custom_print("Repository is *up-to-date*.", rich=True, colors=["green"])
        
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o comando Git: {e}")
        except FileNotFoundError:
            print("Git não encontrado. Verifique se está instalado e disponível no PATH.")