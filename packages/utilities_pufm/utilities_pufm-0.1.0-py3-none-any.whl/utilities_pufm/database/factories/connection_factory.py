#* Imports
import os
#* Imports dos módulos
from utilities_pufm.database.enums import SGBDType
from utilities_pufm.database.db_connection.pg_connection import PgConnection
from utilities_pufm.database.db_connection.mysql_connection import MySQLConnection

def get_connection(name: str, **kargs):
     sgbd_type = os.getenv(f"{name}_TYPE")
     if sgbd_type == SGBDType.TYPE_MYSQL.value:
          return MySQLConnection(name=name, **kargs)
     elif sgbd_type == SGBDType.TYPE_POSTGRES.value:
          return PgConnection(name=name, **kargs)
     print("[CONNECTION]: Tipo de conecção desconhecida.")
     return None