from pyspark.sql import SparkSession, DataFrame
from spark_jdbc_reader.exceptions import (
    JDBCConnectionError, TableReadError, QueryExecutionError
)


class JDBCReader:
    def __init__(self, host: str, user: str, password: str, port: int = 3306,database: str = None):
        """
        Initializes a JDBCReader instance to connect to a JDBC-compatible database.

        Parameters:
            host (str): Hostname or IP address of the database server.
            user (str): Username for authentication.
            password (str): Password for authentication.
            port (int): Port number of the database. Defaults to 3306.
            database (str, optional): Name of the database to connect to.
        """
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database

        try:
            self.spark = SparkSession.builder.getOrCreate()
        except Exception as e:
            raise JDBCConnectionError("Failed to initialize SparkSession.") from e

    def _build_jdbc_url(self, with_db: bool = True) -> str:
        db_part = f"/{self.database}" if with_db and self.database else ""
        return f"jdbc:mysql://{self.host}:{self.port}{db_part}"

    def read_table(self, table_name: str) -> DataFrame:
        """
        Reads a table from the specified database.

        Parameters:
            table_name (str): Name of the table to read.

        Returns:
            DataFrame: A Spark DataFrame containing the table data.
        """
        if not self.database:
            raise TableReadError("Database name must be specified to read a table.")

        try:
            return self.spark.read \
                .format("jdbc") \
                .option("url", self._build_jdbc_url(with_db=True)) \
                .option("dbtable", table_name) \
                .option("user", self.user) \
                .option("password", self.password) \
                .load()
        except Exception as e:
            raise TableReadError(f"Failed to read table '{table_name}'.") from e

    def execute_query(self, query: str) -> DataFrame:
        """
        Executes a raw SQL query on the database.

        Parameters:
            query (str): SQL query string to execute.

        Returns:
            DataFrame: A Spark DataFrame containing the query results.
        """
        try:
            return self.spark.read \
                .format("jdbc") \
                .option("url", self._build_jdbc_url(with_db=False)) \
                .option("query", query) \
                .option("user", self.user) \
                .option("password", self.password) \
                .load()
        except Exception as e:
            raise QueryExecutionError(f"Failed to execute query:\n{query}") from e
