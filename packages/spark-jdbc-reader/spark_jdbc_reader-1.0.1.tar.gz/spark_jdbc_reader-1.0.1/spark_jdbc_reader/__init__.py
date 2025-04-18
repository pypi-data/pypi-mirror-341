# spark_jdbc_reader/__init__.py
from .reader import JDBCReader

def read_table(host, user, password, database, table_name, port=3306):
    """
    Fetches an entire table from a JDBC-compatible database.

    Parameters:
        host (str): The hostname or IP address of the database server.
        user (str): Username used for database authentication.
        password (str): Password for the user.
        database (str): Name of the target database.
        table_name (str): Name of the table to be read.
        port (int, optional): Port number for the database connection. Defaults to 3306.

    Returns:
        pyspark.sql.DataFrame: A DataFrame containing the contents of the specified table.

    Example:
        >>> from spark_jdbc_reader import read_table
        >>> df = read_table("localhost", "admin", "secret", "my_db", "employees", port=5432)
        >>> df.show()
    """
    reader = JDBCReader(host, user, password, database, port)
    return reader.read_table(table_name)

def execute_query(host, user, password, query, port=3306):
    """
    Executes a raw SQL query on a JDBC-compatible database and returns the results.

    Parameters:
        host (str): The hostname or IP address of the database server.
        user (str): Username used for database authentication.
        password (str): Password for the user.
        query (str): The SQL query to execute.
        port (int, optional): Port number for the database connection. Defaults to 3306.

    Returns:
        pyspark.sql.DataFrame: A DataFrame containing the result of the executed query.

    Example:
        >>> from spark_jdbc_reader import execute_query
        >>> df = execute_query("localhost", "admin", "secret", "SELECT * FROM employees WHERE salary > 50000", port=5432)
        >>> df.show()
    """
    reader = JDBCReader(host, user, password, port)
    return reader.execute_query(query)
