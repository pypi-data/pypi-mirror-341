import sys
from io import StringIO
from collections import deque

class LogRedirector:
    def __init__(self, update_log_func):
        """
        Redireciona mensagens de print para o painel de log customizado.

        Args:
            update_log_func (callable): Função para atualizar o painel de log.
        """
        self.update_log_func = update_log_func
        self.original_stdout = sys.stdout
        self.buffer = StringIO()

    def write(self, message):
        # Remove novas linhas para evitar mensagens vazias
        if message.strip():
            self.update_log_func(message.strip())

    def flush(self):
        """Necessário para compatibilidade com sys.stdout."""
        pass

    def start(self):
        """Inicia o redirecionamento."""
        sys.stdout = self

    def stop(self):
        """Restaura o stdout original."""
        sys.stdout = self.original_stdout
        
class RichLogger():
    _instance = None
    def __init__(self):
        self.messages = deque(["[bold white]Log:[/bold white]"])
        self.size = 20

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def write(self, message):
        self.messages.extend(message.splitlines())
        while len(self.messages) > self.size:
            self.messages.popleft()

    def flush(self):
        pass