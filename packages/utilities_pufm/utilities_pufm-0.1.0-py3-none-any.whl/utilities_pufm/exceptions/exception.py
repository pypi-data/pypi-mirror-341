class MigrationError(Exception):
    """
    Exceção personalizada para erros durante o processo de migração.
    """
    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details

    def __str__(self):
        if self.details:
            return f"{self.args[0]} | Detalhes: {self.details}"
        return self.args[0]
