def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        sql_query = file.read()
    return sql_query