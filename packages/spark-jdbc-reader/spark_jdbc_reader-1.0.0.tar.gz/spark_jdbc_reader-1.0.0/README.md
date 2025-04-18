# spark-jdbc-reader

A lightweight JDBC utility for reading SQL tables and queries into PySpark DataFrames.

## Installation

```bash
pip install spark-jdbc-reader

```python
from spark_jdbc_reader.reader import JDBCReader
reader = JDBCReader("localhost", 3306, "my_db", "user", "pass")
df = reader.read_table("my_table")
df.show()