# spark-jdbc-reader

A lightweight JDBC utility for reading SQL tables and queries into PySpark DataFrames.

## Installation

```bash
pip install spark-jdbc-reader

Usage

from spark_jdbc_reader import read_table
df = read_table("localhost", "admin", "secret", "my_db", "employees", port=5432)
df.show()

from spark_jdbc_reader import execute_query
df = execute_query("localhost", "admin", "secret", "SELECT * FROM employees WHERE salary > 50000", port=5432)
df.show()

