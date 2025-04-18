import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from typing import Dict, Tuple, Optional
from uuid import uuid4

class PgConnection:
    def __init__(self, name, pool_size=5, max_overflow=10, pool_timeout=30, pool_recycle=3600, multithread: bool = False) -> None:
        
        self.name = name
        self.session_info: Dict = {}
        self.multi_thread = multithread
        
        try:
            print(f"[POSTGRES-CONNECTION]: Iniciando processo de conexão com {name}...")

            self.connection_params = {
                "dbname": os.getenv(f"{name}_DB_NAME"),
                "user": os.getenv(f"{name}_USER"),
                "password": os.getenv(f"{name}_PASSWORD"),
                "host": os.getenv(f"{name}_HOST"),
                "port": os.getenv(f"{name}_PORT"),
            }

            if None in self.connection_params.values():
                missing = [k for k, v in self.connection_params.items() if v is None]
                raise ValueError(f"Missing environment variables: {', '.join(missing)}")

            print("[POSTGRES-CONNECTION]: Parâmetros:\n" + "\n".join([f"{key}: {val}" for key, val in self.connection_params.items()]))

            # Cria a string de conexão para SQLAlchemy
            self.connection_url = (
                f"postgresql://{self.connection_params['user']}:{self.connection_params['password']}@"
                f"{self.connection_params['host']}:{self.connection_params['port']}/{self.connection_params['dbname']}"
            )
            
            self.engine = create_engine(
                self.connection_url,
                pool_size=0,
                max_overflow=max_overflow,
                pool_timeout=pool_timeout,
                pool_recycle=pool_recycle,
                pool_pre_ping=True
            )
            
            self.Session = sessionmaker(bind=self.engine)
            self.session_factory = scoped_session(self.Session)
            print("[POSTGRES-CONNECTION]: Conexão estabelecida com sucesso usando SQLAlchemy.")

            self.poll_sessions = {
            }
            
        except Exception as e:
            print(f"[POSTGRES-CONNECTION]: Nome: {self.name}. Erro ao conectar ao Postgres: {e}")
            self.engine = None
            self.Session = None
            raise

    def get_engine(self):
        return self.engine

    def get_session(self, session_id: str) -> Tuple[str, Session]:
        if session_id in self.session_info:
            session = self.session_info[session_id]
            return session
        return None

    def get_new_session(self) -> Tuple[str, Session]:
        session_id = str(uuid4())
        if self.multi_thread:
            session = self.session_factory()
        else:
            session = self.Session()
        
        self.session_info[session_id] = [session, True]
        
        return session_id, session
    
    def close_session(self, session_id: str) -> bool:
        if session_id in self.session_info:
            dropped = self.session_info.pop(session_id, None)
            try:
                dropped[1] = False
                dropped[0].close()
                print(f"[POSTGRES-CONNECTION-{self.name}]: Session {session_id[:8]} closed.")
                return True
            except Exception as e:
                print(f"[POSTGRES-CONNECTION-error-{self.name}]: Error closing session {session_id[:8]}: {e}")
        return False

    def close_sessions(self, session_ids: list[str]) -> None:
        for session_id in session_ids:
            self.close_session(session_id)
            
    def close_all_sessions(self) -> None:
        session_ids = list(self.session_info.keys())
        self.close_sessions(session_ids)
        
    def close_all(self) -> None:
        self.close_all_sessions()
        if self.engine:
            self.engine.dispose()
            print(f"[POSTGRES-CONNECTION-{self.name}]: Engine disposed")

    def get_open_sessions_id(self) -> list[str]:
        return [session_id for session_id, (session, status) in self.session_info.items() if status]
    
    def check_for_closed_sessions(self):
        for session_id, session_status in self.session_info.items():
            if not session_status[1]:
                self.close_session(session_id)
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_all()