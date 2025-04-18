import os
import subprocess
import textwrap
import logging

from datetime import date 
from sqlalchemy import text, inspect, insert, MetaData, types, select
from sqlalchemy.orm import Session
from rich.progress import Progress
from utilities_pufm.prints.rich import custom_print
from utilities_pufm.database.db_connection.pg_connection import PgConnection
from sqlalchemy.engine import RowMapping
from utilities_pufm.files import files
from typing import List, Any, Dict, Union, Tuple

def execute_sql_query(sql_query, session: Session, params: dict = None, is_text: bool = False):
    
    try:
        if params:
            result = session.execute(sql_query if is_text else text(sql_query), params)
        else:
            result = session.execute(sql_query if is_text else text(sql_query))
        
        #TODO: Dve ser somente um tipo. Para não ter que fazer a conversão aqui para string.
        if is_text:
            sql_query = get_str_from_sqlalchemy_stmt(sql_query)
            # print(f"[EXECUTION-QUERY] Query:\n{sql_query}\n")
        
        if sql_query.strip().upper().startswith("SELECT"):
            results = result.fetchall()
            column_names = result.keys()
            
            return results, column_names
        elif sql_query.strip().upper().startswith("INSERT"):
            session.commit()    
            # custom_print(f"*[EXECUTION-QUERY]* Executando query:\n{sql_query}")
            
            insert_id = result.scalar()
            # custom_print(f"*[EXECUTION-QUERY]* ultimo ID:\n{insert_id}", colors=["red"])
            return insert_id, True
        
        elif any(sql_query.strip().upper().startswith(cmd) for cmd in ["UPDATE", "DELETE", "DROP", "REVOKE", "GRANT"]):
            session.commit()  # Commit necessário após alterações
            return result.rowcount, True
        
        elif any(sql_query.strip().upper().startswith(cmd) for cmd in ["SET", "ALTER"]):
            session.commit()
            return None, True
        
        elif sql_query.strip().upper().startswith("SHOW"):
            results = result.fetchall()
            return results, True
        
        return result.fetchall(), True
    
    except Exception as e:
        print(f"[EXECUTION] Erro na execução do script SQLAlchemy: {e}\n Query: {sql_query}")
        session.rollback()  # Faz o rollback em caso de erro
        files.save_file(f"./data/{date.today()}-ERRORS.txt", f"[ERROR]\n[EXECUTION] Erro na execução do script SQLAlchemy: {e}\n[SQL]: {sql_query}\n\n", how = "a")
        return f"Erro: {str(e)}", None
    

########################## Checking ##########################
def is_table_exists(session, table_name) -> bool:
    schema, table = table_name.split(".")
        
    query = textwrap.dedent("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_schema = :schema
        AND table_name = :table;
    """)

    result, _ = execute_sql_query(sql_query=query, session=session, params={"schema": schema, "table": escape_table_name(table)})
    
    return result[0][0] > 0

def is_line_existes(session: Session, referenced_table, referenced_column, value):
    schema, table = referenced_table.split(".")
    
    query = textwrap.dedent(f"""
        SELECT 1
        FROM {f'{schema}.' if schema else ''}{escape_table_name(table)}
        WHERE {referenced_column} = :value
        LIMIT 1;
    """)

    result = session.execute(query, {"value": value}).fetchone()

    return result is not None

def is_auto_increment(session: Session, table_name: str, column_name: str) -> bool:
    query = textwrap.dedent("""
    SELECT column_name, column_default
    FROM information_schema.columns
    WHERE table_schema = :schema
        AND table_name = :table_name
        AND column_name = :column_name;
    """)
    
    schema, table = table_name.split(".")
    result = execute_sql_query(sql_query=query, session=session, params={
        "schema": schema,
        "table_name": f"{schema}.{escape_table_name(table)}",
        "column_name": column_name}
    )
    
    return result is not None and result[1] is not None and 'nextval' in result[1]

def escape_table_name(table_name: str) -> str:
    if '@' in table_name:
        return f'"{table_name}"'
    return table_name

########################## Get Information ##########################
def get_all_rows(session, table_name):
    """
        Retrieve all rows from a specified table in the database.

        Args:
            session (Session): The SQLAlchemy session used to connect to the database.
            table_name (str): The name of the table from which to fetch all rows.

        Returns:
            tuple: A tuple containing the results as a list of rows and the column names.
    """
    schema, table = table_name.split(".")
    sql_query = textwrap.dedent(f"""
        SELECT *
        FROM {schema}.{escape_table_name(table)};
    """)
    return execute_sql_query(sql_query=sql_query, session=session)

def take_referenced_rows(session: Session, referenced_table: str, referenced_column: str, value: Union[str, List[str]]):
    """
    Retrieve all rows from a specified table in the database that matches the specified value(s)
    in the referenced column.

    Args:
        session (Session): The SQLAlchemy session used to connect to the database.
        referenced_table (str): The name of the table that contains the referenced column.
        referenced_column (str): The name of the column that contains the reference value.
        value (str or list): The value or list of values to filter the rows by.

    Returns:
        tuple: A tuple containing the results as a list of rows and the column names.
    """
    schema, table = referenced_table.split(".")
    query = textwrap.dedent(f"""
        SELECT *
        FROM {schema}.{escape_table_name(table)}
        WHERE {referenced_column} = :value;
    """) if not isinstance(value, list) else textwrap.dedent(f"""
        SELECT *
        FROM {schema}.{escape_table_name(table)}
        WHERE {referenced_column} = ANY(:value);
    """)
    
    return execute_sql_query(sql_query=query, session=session, params={'value': value})

def count_foreign_references(session, table_name) -> List:
    """
    Conta quantas vezes uma tabela é referenciada como chave estrangeira em outras tabelas.
    
    :param session: Sessão do SQLAlchemy.
    :param schema: Esquema da tabela.
    :param table: Nome da tabela.
    :return: Lista de dicionários contendo as tabelas que referenciam e a contagem de referências.
    """
    
    schema, table = table_name.split('.')
    query = textwrap.dedent("""
        SELECT 
            tc.table_schema, 
            tc.table_name, 
            COUNT(tc.constraint_name) AS reference_count
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
            AND kcu.table_schema = :schema
            AND kcu.table_name = :table
        GROUP BY tc.table_schema, tc.table_name
        ORDER BY reference_count DESC;
    """)
    
    result = session.execute(text(query), {'schema': schema, 'table': table}).fetchall()
    
    return [{'schema': row.table_schema, 'table': row.table_name, 'count': row.reference_count} for row in result]

def index_exists(session: Session, index_complete_name: str):
    schema, index_name = index_complete_name.split(".")
    result = session.execute(text(f"""
        SELECT indexname 
        FROM pg_indexes 
        WHERE schemaname = '{schema}' 
        AND indexname = '{index_name}';
    """))
    return result.scalar() is not None  # Retorna True se o índice existir

def drop_index(session: Session, index_complete_name: str):
    if index_exists(session=session, index_complete_name=index_complete_name):    
        session.execute(text(f"DROP INDEX {index_complete_name};"))
        session.commit()

def create_index(session: Session, index_complete_name: str, target_table: str, colums_short_name_list: List[str], where_clouse: str):
    
    _, index_name = index_complete_name.split(".")
    if not index_exists(session=session, index_complete_name=index_complete_name):
        session.execute(text(f"""
            CREATE UNIQUE INDEX {index_name} 
            ON {target_table}
            USING btree ({", ".join(column_short_name for column_short_name in colums_short_name_list)})
            {where_clouse};
        """))
        session.commit()

def get_all_fks(session, table_name):
    """
        Retrieve all foreign keys from a specified table in the database.

        Args:
            session (Session): The SQLAlchemy session used to connect to the database.
            table_name (str): The name of the table from which to fetch all foreign keys.

        Returns:
            list: A list of foreign key information, including the constraint name, constraint definition, source column, foreign key column, and foreign table.
    """
    schema, table = table_name.split(".")

    query_oid = textwrap.dedent("""
        SELECT oid
        FROM pg_class
        WHERE relname = :table
        AND relnamespace = (SELECT oid FROM pg_namespace WHERE nspname = :schema)
    """)

    result_oid, _ = execute_sql_query(sql_query=query_oid, session=session, params={"table": escape_table_name(table), "schema": schema})

    if not result_oid:
        print(f"[QUERY EXEC] Tabela {table_name} não encontrada.")
        return False

    return get_all_fks_for_table_oid(session, result_oid[0][0]) 

def get_all_fks_for_table_oid(session, table_oid):
    query_fks = textwrap.dedent("""
        SELECT
            conname AS constraint_name,
            pg_catalog.pg_get_constraintdef(r.oid, true) AS constraint_definition,
            att1.attname AS source_column,
            att2.attname AS foreign_key_column,
            nsp2.nspname || '.' || cl2.relname AS foreign_table
        FROM
            pg_catalog.pg_constraint r
        INNER JOIN
            pg_catalog.pg_class cl ON cl.oid = r.conrelid
        INNER JOIN
            pg_catalog.pg_attribute att1
            ON att1.attnum = ANY(r.conkey) AND att1.attrelid = r.conrelid
        INNER JOIN
            pg_catalog.pg_attribute att2
            ON att2.attnum = ANY(r.confkey) AND att2.attrelid = r.confrelid
        INNER JOIN
            pg_catalog.pg_class cl2 ON cl2.oid = r.confrelid
        INNER JOIN
            pg_catalog.pg_namespace nsp2 ON cl2.relnamespace = nsp2.oid
        WHERE
            r.conrelid = :oid AND r.contype = 'f'
        ORDER BY 1;
    """)
    
    return execute_sql_query(sql_query=query_fks, session=session, params={"oid": table_oid})

def get_primary_keys(session: Session, table_name):
    schema, table = table_name.split(".")
    
    inspector = inspect(session.get_bind())
    constraint_pk = inspector.get_pk_constraint(table, schema=schema)
    
    return constraint_pk["constrained_columns"] if constraint_pk["constrained_columns"] else None

def update_null_inline(
    session: Session,
    table_name: str,
    attribute_name: Union[str, List[str]],
    attribute_value: Union[str, int, List[Union[str, int]]],
    data_dict: Dict
) -> Tuple[bool, str]:

    """
    Execute an update statement with the given set and where clauses.

    Args:
        session (Session): The SQLAlchemy session used to connect to the database.
        table_name (str): The name of the table to update.
        attribute_name (Union[str, List[str]]): The name of the column(s) to update.
        attribute_value (Union[str, int, List[Union[str, int]]]): The value(s) to update the column(s) with.
        data_dict (Dict): A dictionary containing the set clauses.

    Returns:
        Tuple[bool, str]: A tuple containing a boolean indicating if the operation was successful and a string with the query executed.
    """
    
    set_clauses = []
    params = {}

    if isinstance(attribute_name, str):
        attribute_name = [attribute_name]
    if not isinstance(attribute_value, list):
        attribute_value = [attribute_value]

    if len(attribute_name) != len(attribute_value):
        raise ValueError("The number of columns in attribute_name does not match the number of values in attribute_value.")

    for column, value in data_dict.items():
        if value is not None:
            set_clauses.append(f"{column} = COALESCE({column}, :{column})")
            params[column] = value

    where_clauses = []
    for i, (col, val) in enumerate(zip(attribute_name, attribute_value)):
        placeholder = f"attr_{i}"
        where_clauses.append(f"{col} = :{placeholder}")
        params[placeholder] = val

    if set_clauses:
        query = textwrap.dedent(f"""
            UPDATE {table_name}
            SET {', '.join(set_clauses)}
            WHERE {' AND '.join(where_clauses)}
        """)

        return execute_sql_query(sql_query=query, session=session, params=params)
    return -1, False

def get_real_query(check_query, params):
    sql_real = check_query
    for key, value in params.items():
        sql_real = sql_real.replace(f":{key}", f"'{value}'")

    return sql_real

def is_foreign_key_exists(session: Session, table: str, foreign_key_name: str):
    schema, table_name = table.split(".")
    check_query = textwrap.dedent("""
        SELECT 1 
        FROM information_schema.table_constraints 
        WHERE table_schema = :schema
            AND table_name = :table 
            AND constraint_name = :foreign_key_name 
            AND constraint_type = 'FOREIGN KEY';
    """)

    params = {"schema": schema, "table": table_name, "foreign_key_name": foreign_key_name}
    result = session.execute(text(check_query), params).scalar()
    
    # custom_print(f"*[TESTE-is_foreign_key_exists]*: Query: \n{get_real_query(check_query, params)}'\n\n'{bool(result)}'", colors=["red"])
    
    return bool(result)

def drop_foreign_constraint(session: Session, table: str, foreign_key_name: str):
    
    sql_query = textwrap.dedent(f"""
        ALTER TABLE {table}
        DROP CONSTRAINT IF EXISTS {foreign_key_name};
    """)

    return execute_sql_query(sql_query=sql_query, session=session)

def get_max_column_value(session, table_name: str, column_name: str):
    
    sql_query = textwrap.dedent(f"""
        SELECT MAX({column_name}) AS max_value
        FROM {table_name};
    """)
    
    max_val = execute_sql_query(sql_query=sql_query, session=session)
    
    # print(max_val[0][0])
    return max_val[0][0][0] if max_val else None

def get_column_values(session, table_name: str, column_name: str):
    query = select(text(column_name)).select_from(text(table_name))
    result = session.execute(query).scalars().all()
    
    return result if result else []
    
def recreate_foreign_constraint(session, table_origem: str, foreign_key_name: str, column_origem: str, table_destino: str, column_destino: str):
    sql_query = textwrap.dedent(f"""
        ALTER TABLE {table_origem}
        ADD CONSTRAINT {foreign_key_name}
        FOREIGN KEY ({column_origem}) 
        REFERENCES {table_destino}({column_destino});
    """)

    return execute_sql_query(sql_query=sql_query, session=session)

def get_columns_names_and_types(session, table_name):
    
    schema, table = table_name.split(".")
    
    inspector = inspect(session.get_bind())
    columns = inspector.get_columns(table, schema=schema)

    return [(col['name'], col['type']) for col in columns]

def get_str_from_sqlalchemy_stmt(stmt):
    return str(stmt.compile())

########################## Set information ##########################
def insert_row(session: Session, columns: List[str], values: List[Any], table_name: str) -> None:
    schema, table = table_name.split(".")
    
    if len(columns) != len(values):
        raise ValueError("The number of values on columns and values must be the same.")

    engine = session.get_bind()
    if not hasattr(engine, '_metadata_cache'):
        engine._metadata_cache = {}

    table_escaped = escape_table_name(table)
    
    metadata_key = f"{schema}.{table_escaped}" if schema else table_escaped
    if metadata_key not in engine._metadata_cache:
        metadata = MetaData()
        metadata.reflect(schema=schema, bind=engine, only=[table_escaped])
        engine._metadata_cache[metadata_key] = metadata
    else:
        metadata = engine._metadata_cache[metadata_key]

    qualified_name = f"{schema}.{table_escaped}" if schema else table_escaped
    table_obj = metadata.tables.get(qualified_name)
    if table_obj is not None:
        try:
            data = dict(zip(columns, values))
            stmt = insert(table_obj).values(data).returning(table_obj.primary_key.columns)
            result = execute_sql_query(sql_query=stmt, session=session, is_text=True)
            return result, get_real_query(get_str_from_sqlalchemy_stmt(stmt), data)
        except Exception as e:
            logging.error(f"Erro ao inserir na tabela {table_name}: {str(e)}")
            raise
    else:    
        raise ValueError(f"Table '{qualified_name}' not found")

########################## Backups e Restaurations ##########################
def backup_all_individual_tables(
    conn,
    backup_dir: str,
    verbose: bool = False,
    progress_bar: Progress = None,
    return_verbose: bool = False
) -> bool:

    os.makedirs(backup_dir, exist_ok=True)
    session_id, session = conn.get_new_session()
    verbose_list = []
    status_list = []
    
    tables, _ = execute_sql_query(
        sql_query=textwrap.dedent(
            """
            SELECT schemaname, tablename
            FROM pg_tables
            WHERE schemaname NOT IN ('pg_catalog', 'information_schema');
            """
        ),
        session=session
    )
    progress_bar.start()
    backup_task = progress_bar.add_task(description="[bold yellow]Backup[/bold yellow] em progresso...", total=len(tables))
    for schema_name, table_name in tables:
        
        bkp_result = backup_table(
            conn=conn,
            schema_name=schema_name,
            table_name=table_name,
            backup_dir=backup_dir,
            verbose=verbose,
            return_verbose=return_verbose
        )
        if return_verbose:
            status_bkp, verbose_list_table, _ = bkp_result
        else:
            status_bkp, _ = bkp_result
        
        verbose_list.extend(verbose_list_table)
        status_list.append(status_bkp)
        
        progress_bar.update(backup_task, advance=1)
    progress_bar.stop()
        
    if any(not status for status in status_list):
        verbose_str = "Pelo menos um 'backup' falhou."
    else:
        verbose_str = "Backup de todas as tabelas de todos os esquemas concluído com sucesso."
    if verbose:
        print(verbose_str)
    if return_verbose:
        verbose_list.append(verbose_str)
    
    conn.close_session(session_id)
    if return_verbose:
        return True, verbose_list
    return True

def backup_table(conn, db: str, schema_name: str, table_name: str, backup_dir: str, verbose: bool = False, return_verbose: bool = False):
    verbose_list = []
    
    backup_file_name = f"{db}_{schema_name}_{table_name}_backup.sql"
    backup_file_path = os.path.join(backup_dir, backup_file_name)

    engine = conn.get_engine()
    
    verbose_str = f"Iniciando backup da tabela {schema_name}.{table_name}..."
    if verbose:
        print(verbose_str)
    if return_verbose:
        verbose_list.append(verbose_str)

    connection_info = engine.url
    command = (
        f"pg_dump -h {connection_info.host} -U {connection_info.username} -d {connection_info.database} "
        f"-t {schema_name}.{table_name} -f {backup_file_path} --clean --if-exists --column-inserts --disable-triggers"
    )

    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        verbose_str = f"Erro ao fazer backup da tabela {schema_name}.{table_name}."
        print(verbose_str)
        if return_verbose:
            verbose_list.append(verbose_str)
            return False, verbose_list, backup_file_path
        else:
            return False, backup_file_path

    verbose_str = f"Backup da tabela {schema_name}.{table_name} concluído com sucesso."
    if verbose:
        print(verbose_str)
    if return_verbose:
        verbose_list.append(verbose_str)
        return True, verbose_list, backup_file_path
    else:
        return True, backup_file_path

def backup_all_database(
    backup_dir: str,
    db_name: str,
    conn = None,
    verbose: bool = False,
    return_verbose: bool = False,
    pg_path: str = None,
    params: dict = None,
    include_roles: bool = True
) -> bool:

    # print(f"[PARAMETERS]:\n{params}")
    
    if conn is None and params is None:
        raise ValueError("Nenhuma conexão ou parâmetros de conexão fornecidos.")
    
    if conn is not None:
        engine = conn.get_engine()    
        connection_info = engine.url
        host = connection_info.host
        username = connection_info.username
        os.environ['PGPASSWORD'] = connection_info.password
        database = connection_info.database
    elif params is not None:
        host = params['host']
        username = params['username']
        database = params['database']
        os.environ['PGPASSWORD'] = params['password']
        
    os.makedirs(backup_dir, exist_ok=True)

    backup_file_name = f"{db_name}_backup-all.dump"
    backup_file_path = os.path.join(backup_dir, backup_file_name)
    
    verbose_list = []
    verbose_str = f"Iniciando backup completo do banco de dados {db_name}..."
    if verbose:
        print(verbose_str)
    if return_verbose:
        verbose_list.append(verbose_str)
    
    pg_bin_path = ''
    if pg_path:
        pg_bin_path = f'"{pg_path}"'
    
    dump_command = (
        f"{pg_bin_path}pg_dump -h {host} -U {username} -d {database} "
        f"-f {backup_file_path} -Fc --clean --if-exists --column-inserts --create"
    )

    dump_result = subprocess.run(dump_command, shell=True)

    if include_roles:
        role_backup_file_name = "roles_backup-all.dump"    
        role_backup_file_path = os.path.join(backup_dir, role_backup_file_name)
        
        roles_command = (
            f"{pg_bin_path}pg_dumpall -h {host} -U {username} --roles-only "
            f"-f {role_backup_file_path}"
        )

        roles_result = subprocess.run(roles_command, shell=True)
    
    if dump_result.returncode != 0:
        verbose_str = f"Erro ao fazer backup completo do banco de dados {db_name}."
        if verbose:
            print(verbose_str)
        if return_verbose:
            verbose_list.append(verbose_str)
            
        return False, verbose_list
    elif include_roles and roles_result.returncode != 0:
        verbose_str = f"Erro ao fazer backup dos papéis do banco de dados {db_name}."
        if verbose:
            print(verbose_str)
        if return_verbose:
            verbose_list.append(verbose_str)
            
        return False, verbose_list

    if verbose:
        verbose_str = f"Backup completo do banco de dados {db_name} concluído com sucesso. Backup salvo em {backup_file_path}."
        if include_roles:
            verbose_str += f" Backup dos papéis também concluído. Backup salvo em {role_backup_file_path}."
        
        if verbose:
            print(verbose_str)
        if return_verbose:
            verbose_list.append(verbose_str)

    if return_verbose:
        return True, verbose_list
    return True

def restore_all_database(conn, backup_dir: str, bd_name: str, new_terminal: bool = False, verbose: bool = True, return_verbose: bool = False, pg_path: str = None, include_roles: bool = True) -> bool:
    
    file_restore_path = os.path.join(backup_dir, bd_name + "_backup-all.dump")
    
    engine =  conn.get_engine()
    connection_info = engine.url
    if return_verbose:
        verbose_list = []
    
    verbose_str = f"[RESTORE]: Initializing restore process from {file_restore_path}... "
    if verbose:
        print(verbose_str)
    if return_verbose:
        verbose_list.append(verbose_str)
    
    conn.close_all_sessions()
    
    verbose_str = "[RESTORE]: Trying to restore database..."
    if verbose:
        print(verbose_str)
    if return_verbose:
        verbose_list.append(verbose_str)
    
    pg_bin_path = ''
    if pg_path:
        pg_bin_path = f'"{pg_path}"'
        
    dropdb_command = f"{pg_bin_path}dropdb -h {connection_info.host} -U {connection_info.username} --force {connection_info.database}"
    result = subprocess.run(dropdb_command, shell=True, text=True, capture_output=True)
    
    if result.returncode != 0:
        verbose_str = f"[RESTORE]: Warning during drop database: {result.stderr}"
        if verbose:
            print(verbose_str)
        if return_verbose:
            verbose_list.append(verbose_str)
    else:
        verbose_str = "[RESTORE]: Database dropped successfully"
        if verbose:
            print(verbose_str)
        if return_verbose:
            verbose_list.append(verbose_str)
    
    if include_roles:
        role_backup_file_name = "roles_backup-all.dump"    
        role_backup_file_path = os.path.join(backup_dir, role_backup_file_name)
        
        roles_command = (
            f"{pg_bin_path}psql -h {connection_info.host} -U {connection_info.username} -f {role_backup_file_path}"
        )

        roles_result = subprocess.run(roles_command, shell=True)
    
        if roles_result.returncode != 0:
            verbose_str = f"[RESTORE-restore]: Warning during roles restoring: {roles_result.stderr}"
            if verbose:
                print(verbose_str)
            if return_verbose:
                verbose_list.append(verbose_str)
        else:
            verbose_str = "[RESTORE-restore]: Roles restored successfully!"
            if verbose:
                print(verbose_str)
            if return_verbose:
                verbose_list.append(verbose_str)
    
    createdb_command = f"{pg_bin_path}createdb -h {connection_info.host} -U {connection_info.username} {connection_info.database}"
    result = subprocess.run(createdb_command, shell=True, text=True, capture_output=True)
    
    if result.returncode != 0:
        verbose_str = f"[RESTORE]: Warning during create database: {result.stderr}"
        if verbose:
            print(verbose_str)
        if return_verbose:
            verbose_list.append(verbose_str)
    else:
        verbose_str = "[RESTORE]: Database created successfully"
        if verbose:
            print(verbose_str)
        if return_verbose:
            verbose_list.append(verbose_str)
    
    command = f"{pg_bin_path}pg_restore --disable-triggers -v --clean --if-exists --create --jobs=10 -U postgres -d postgres {file_restore_path}"

    if new_terminal:
        command = f'start cmd /K "{command}"'

    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        
        success = result.returncode == 0
        status_msg = "[RESTORE]: Restore to database was completed successfully." if success else "[RESTORE]: Restore failed."
        
        if verbose:
            print(status_msg)
        if return_verbose:
            verbose_list.append(status_msg)
            return success, verbose_list
            
        return success
        
    except Exception as e:
        error_msg = f"[RESTORE]: An error occurred during restore: {str(e)}"
        if verbose:
            print(error_msg)
        if return_verbose:
            verbose_list.append(error_msg)
            return False, verbose_list
        return False
    
    finally:
        #TODO: Verificar qual é a sessião que deve continuar aberta
        conn.get_new_session()
        verbose_str = "[RESTORE]: Session restarted. Restore terminated succefully."
        if verbose:
            print(verbose_str)
        if return_verbose:
            verbose_list.append(verbose_str)

def restore_table(conn: PgConnection, backup_file: str, table: str, pg_path: str = None, verbose: bool = True, return_verbose: bool = False):
    
    inspector = inspect(conn.get_engine())
    
    if table in inspector.get_table_names():
        session_id, session = conn.get_new_session()
        session.execute(text(f"DELETE FROM {table};"))
        session.commit()
        conn.close_session(session_id=session_id)
        print(f"All registers from {table} were deleted.")
    else:
        print(f"Table {table} does not exist in the database {conn.get_engine().url}.")
    
    pg_bin_path = ''
    if pg_path:
        pg_bin_path = f'"{pg_path}"'
    
    #* restaurar o estado da tabela anterior
    command = f"{pg_bin_path}pg_restore --disable-triggers -v --clean --if-exists --create --jobs=10 -U postgres -d postgres -t {table} {backup_file}"
    
    if return_verbose:
        verbose_list = []
    
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        success = result.returncode == 0
        
        status_msg = "[RESTORE]: Restore to database was completed successfully." if success else "[RESTORE]: Restore failed."
    
        if verbose:
            print(status_msg)
        if return_verbose:
            verbose_list.append(status_msg)
            return success, verbose_list
            
        return success
        
    except Exception as e:
        error_msg = f"[RESTORE]: An error occurred during restore: {str(e)}"
        if verbose:
            print(error_msg)
        if return_verbose:
            verbose_list.append(error_msg)
            return False, verbose_list
        return False
    
    finally:
        
        verbose_str = f"[RESTORE]: Table {table} restored successfully."
        if verbose: 
            print(verbose_str)
        if return_verbose:
            verbose_list.append(verbose_str)
            return success, verbose_list
        return success
    
    