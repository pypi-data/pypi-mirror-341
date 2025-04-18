from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

class MySQLConnection:
    def __init__(self, name):
        try:
            print(f"[MYSQL-CONECTION]: Iniciando processo de conexão com {name}...")

            # Obtenção dos parâmetros de conexão a partir de variáveis de ambiente
            self.connection_params = {
                "user": os.getenv(f"{name}_USER"),
                "password": os.getenv(f"{name}_PASSWORD"),
                "host": os.getenv(f"{name}_HOST"),
                "port": os.getenv(f"{name}_PORT"),
                "database": os.getenv(f"{name}_DB_NAME"),
            }

            # Verificar se todos os parâmetros estão presentes
            for key, value in self.connection_params.items():
                if value is None:
                    raise ValueError(f"[MYSQL-CONECTION]: Parâmetro {key} não encontrado nas variáveis de ambiente")

            # Construir a URL de conexão para o SQLAlchemy
            self.connection_url = (
                f"mysql+pymysql://{self.connection_params['user']}:{self.connection_params['password']}"
                f"@{self.connection_params['host']}:{self.connection_params['port']}/{self.connection_params['database']}"
            )
            print(f"[MYSQL-CONECTION]: Conectando usando URL: {self.connection_url}")

            # Criar engine do SQLAlchemy
            self.engine = create_engine(self.connection_url)
            self.Session = sessionmaker(bind=self.engine)

            # Testar conexão
            with self.engine.connect() as conn:
                print("[MYSQL-CONECTION]: Conexão estabelecida com sucesso.")

            self.session = None  # Sessão será criada sob demanda

        except Exception as e:
            print(f"[MYSQL-CONECTION]: Falha na conexão. Erro: {e}")
            raise

    def get_session(self):
        """Cria e retorna uma nova sessão."""
        if self.session is None:
            self.session = self.Session()
            print("[MYSQL-CONECTION]: Sessão criada.")
        return self.session

    def close_session(self):
        """Fecha a sessão, se existir."""
        if self.session:
            self.session.close()
            print("[MYSQL-CONECTION]: Sessão fechada.")
            self.session = None

    def close_engine(self):
        """Fecha o engine do SQLAlchemy."""
        if self.engine:
            self.engine.dispose()
            print("[MYSQL-CONECTION]: Engine fechado.")

    def close_all(self):
        """Fecha sessão e engine."""
        self.close_session()
        self.close_engine()
