import textwrap
from sqlalchemy import text
from sqlalchemy.orm import Session
import os
import subprocess
import pandas as pd
from utilities.strings.strings import join_values
from utilities.prints.rich import custom_print

def execute_sql_query(sql_query, session: Session, params: dict = None):
    try:
        if params:
            result = session.execute(text(sql_query), params)
        else:
            result = session.execute(text(sql_query))
        
        if sql_query.strip().upper().startswith("SELECT"):
            results = result.fetchall()
            column_names = result.keys()
            
            return results, column_names
        elif sql_query.strip().upper().startswith("INSERT"):
            session.commit()    
            # Importante: MySQL precisa do commit explícito
            insert_id = result.lastrowid
            
            return insert_id, True
        
        elif any(sql_query.strip().upper().startswith(cmd) for cmd in ["UPDATE", "DELETE", "DROP"]):
            session.commit()  # Commit necessário após alterações
            return result.rowcount, True
        
        elif sql_query.strip().upper().startswith("SET"):
            session.commit()
            return None, True
        
        elif sql_query.strip().upper().startswith("SHOW"):
            results = result.fetchall()
            return results, True
        
        return result.fetchall(), True
    
    except Exception as e:
        print(f"[EXECUTION] Erro na execução do script SQLAlchemy: {e}\n Query: {sql_query}")
        session.rollback()  # Faz o rollback em caso de erro
        return f"Erro: {str(e)}", None


def get_all_rows(session, tabela):
    sql_query = f"""
        SELECT *
        FROM `{tabela}`;
    """
    
    return execute_sql_query(sql_query=sql_query, session=session)

def get_column_value_by_condition(session, table, target_column, condition_column, condition_value):
    """
    Retorna os valores de uma coluna específica onde outra coluna atende a uma condição.

    Args:
        session: A sessão SQLAlchemy.
        tabela: O nome da tabela.
        target_column: A coluna cujo valor será retornado.
        condition_column: A coluna que será usada na condição.
        condition_value: O valor da condição.

    Returns:
        Uma lista de valores da target_column que atendem à condição.
    """
    
    if isinstance(condition_value, str):
        condition_value = f"'{condition_value}'"
    elif condition_value is None:
        condition_value = "NULL"
        
    sql_query = f"""
        SELECT {target_column}
        FROM `{table}`
        WHERE {condition_column} = {condition_value};
    """

    result_val, columns = execute_sql_query(sql_query=sql_query, session=session)
    
    if result_val:
        return result_val[0][0], columns  # Retorna o valor encontrado na primeira linha e primeira coluna
    else:
        return None, None

def check_value_exists(session, table_name, column_name, value):
    query_check_value = textwrap.dedent(f"""
    SELECT *
    FROM {table_name}
    WHERE {column_name} = :value
    """)

    params = {"value": value}

    results, columns = execute_sql_query(sql_query=query_check_value, session=session, params=params)
    
    return pd.DataFrame(data=results, columns=columns), True if results else False

def get_chave_primaria(session, table_name):
    query_find_primary_key = f"""
    SELECT COLUMN_NAME
    FROM information_schema.KEY_COLUMN_USAGE
    WHERE TABLE_NAME = '{table_name}'
        AND CONSTRAINT_NAME = 'PRIMARY';
    """

    results, _ = execute_sql_query(sql_query=query_find_primary_key, session=session)

    return results[0][0] if results else None

def insert_row(session, columns, list_values, tabela):
    
    # print(f"[TESTE-INSERT]: {list_values}")
    
    list_values = [
        valor.item() if isinstance(valor, pd.Series) else valor
        for valor in list_values
    ]
    
    insert_statement = textwrap.dedent(f"""
    INSERT INTO {tabela} ({', '.join(columns)}) 
    VALUES ({join_values(list_of_values=list_values)});
    """)

    # print(f"[TESTE-INSERT]: {insert_statement}")
    
    return execute_sql_query(sql_query=insert_statement, session=session)

def update_row(session, tabela, column_to_change, value_to_set, condition_column, condition_value, logic_operand):
    
    value_to_set_str = f"'{value_to_set}'" if isinstance(value_to_set, str) else value_to_set
    condition_value_str = f"'{condition_value}'" if isinstance(condition_value, str) else condition_value
    
    update_statement = textwrap.dedent(
        f"""
        UPDATE {tabela}
        SET {column_to_change} = {value_to_set_str}
        WHERE {condition_column} {logic_operand} {condition_value_str};
        """
    )
    # print(f"[TESTE]: update_statement: {update_statement}")
    return execute_sql_query(sql_query=update_statement, session=session)

########################## Obter Informações ##########################
def get_columns_names_and_types(session, table_name):
    sql = f"""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = '{table_name}'
    ORDER BY ordinal_position;
    """
    
    resultado, _ = execute_sql_query(sql_query=sql, session=session)
    columns_name = [t[0] for t in resultado]
    columns_type = [t[1] for t in resultado]
    
    return columns_name, columns_type

########################## Backups e Restaurações ##########################
def backup_database(conn, backup_dir: str):
    
    backup_file_name = f"all_{conn.database}_backup.sql"
    backup_file_path = os.path.join(backup_dir, backup_file_name)
    
    if os.path.exists(backup_file_path):
        os.remove(backup_file_path)
        print(f"[BACKUP]: Arquivo '{os.path.abspath(backup_file_path)}' existente apagado.")

    os.environ['MYSQL_PWD'] = conn._password
    
    command = (
        f"mysqldump --skip-lock-tables --routines --add-drop-database --disable-keys "
        f"--extended-insert --comments -u {conn.user} "
        f"--host={conn.server_host} --port={conn.server_port} {conn.database} "
        f"> {backup_file_path}"
    )

    result = subprocess.run(command, shell=True, check=True)
    return backup_file_path, os.path.abspath(backup_file_path), result.returncode == 0


def backup_table(conn, tabela, backup_dir):
    backup_file_name = f"{tabela}_backup.sql"
    backup_file_path = os.path.join(backup_dir, backup_file_name)
    if os.path.exists(backup_file_path):
        os.remove(backup_file_path)
        print(
            f"[BACKUP]: Arquivo '{os.path.abspath(backup_file_path)}' existente apagado."
        )
    os.environ['MYSQL_PWD'] = conn._password
    command = (
        f"mysqldump --skip-lock-tables --routines --add-drop-table --disable-keys "
        f"--extended-insert --comments -u {conn.user} "
        f"--host={conn.server_host} --port={conn.server_port} {conn.database} {tabela} "
        f"> {backup_file_path}"
    )

    result = subprocess.run(command, shell=True, check=True)
    return backup_file_path, os.path.abspath(backup_file_path), result.returncode == 0

def restore_table(conn, backup_file):
    if not os.path.exists(backup_file):
        raise FileNotFoundError(f"O arquivo de backup '{backup_file}' não foi encontrado.")
    
    # os.environ['MYSQL_PWD'] = conn.engine._password
    url = conn.engine.url
    user = url.username
    password = url.password
    host = url.host
    port = url.port
    database = url.database
    os.environ['MYSQL_PWD'] = password
    
    command = (
        f"mysql -u {user} "
        f"--host={host} --port={port} "
        f"{database} < {backup_file}"
    )

    result = subprocess.run(command, shell=True, check=True)
    return result.returncode == 0


def restore_all_database(conn, backup_dir):
    relatorio = {}
    
    for file_name in os.listdir(backup_dir):
        if file_name.endswith("_backup.sql") and not file_name.startswith("all_"):
            backup_file = os.path.join(backup_dir, file_name)
            tabela = file_name.replace("_backup.sql", "")
            if os.path.isfile(backup_file):
                status = restore_table(conn, backup_file)
                print(f"[RESTORE]: Restaurado o backup a partir do arquivo '{backup_file}'.")
                if status:
                    relatorio[tabela] = "Sucesso!"
                    print(f"[RESTORE]: Restore do backup a partir do arquivo '{backup_file}' foi bem sucedido.")
                else:
                    relatorio[tabela] = "Falha!"
                    print(f"[RESTORE]: Restore do backup a partir do arquivo '{backup_file}' falhou.")
    
    return relatorio

def delete_all_rows(session, table_name):
    sql = f"DELETE FROM {table_name};"
    return execute_sql_query(sql_query=sql, session=session)

def drop_and_recreate_table(session, table_name):
    # Obter o script completo de criação da tabela
    create_table_script, _ = execute_sql_query(f"SHOW CREATE TABLE {table_name}", session=session)
    
    # custom_print(f"*[DROP]*: Script da *Tabela: {table_name}* criado.", rich=True, colors=["blue"])
    # Dropar a tabela
    _, status = execute_sql_query("SET foreign_key_checks = 0;", session=session)
    custom_print("*[DROP]*: Constraint desativada", rich=True, colors=["blue"])
    num_rows, _ = execute_sql_query(f"DROP TABLE IF EXISTS {table_name}", session=session)
    custom_print(f"*[DROP]*: Tabela: *{table_name}* dropada.", rich=True, colors=["blue"])
    _, status = execute_sql_query("SET foreign_key_checks = 1;", session=session)
    custom_print("*[DROP]*: Constraint ativada", rich=True, colors=["blue"])
    # print(create_table_script)
    # Recriar a tabela usando o script original
    _, recreate_status = execute_sql_query(create_table_script[0][1], session=session)
    custom_print(f"*[RECREATE]*: Tabela: *{table_name}* recriada.", rich=True, colors=["blue"])
    
    _, reset_status = execute_sql_query(f"ALTER TABLE {table_name} AUTO_INCREMENT = 1;", session=session)
    custom_print(f"*[RESET]*: AUTO_INCREMENT da tabela *{table_name}* resetado.", rich=True, colors=["blue"])
    
    return num_rows, recreate_status