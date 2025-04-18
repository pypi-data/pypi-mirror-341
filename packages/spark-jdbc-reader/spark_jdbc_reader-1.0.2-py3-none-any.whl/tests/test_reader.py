import unittest
from unittest.mock import patch, MagicMock
from spark_jdbc_reader.reader import JDBCReader
from spark_jdbc_reader.exceptions import (
    JDBCConnectionError, TableReadError, QueryExecutionError
)


class TestJDBCReader(unittest.TestCase):

    def setUp(self):
        self.host = "localhost"
        self.port = 3306
        self.user = "user"
        self.password = "pass"
        self.database = "test_db"
        self.table_name = "employees"
        self.query = "SELECT * FROM employees"


    @patch('spark_jdbc_reader.reader.SparkSession')
    def test_successful_initialization(self, mock_spark_session):
        mock_spark_session.builder.getOrCreate.return_value = MagicMock()
        reader = JDBCReader(self.host, self.user, self.password, port=self.port, database=self.database)
        self.assertIsNotNone(reader.spark)

    @patch('spark_jdbc_reader.reader.SparkSession')
    def test_initialization_failure_raises_connection_error(self, mock_spark_session):
        mock_spark_session.builder.getOrCreate.side_effect = Exception("Spark failure")
        with self.assertRaises(JDBCConnectionError):
            JDBCReader(self.host, self.user, self.password)
    
    @patch('spark_jdbc_reader.reader.SparkSession')
    def test_read_table_success(self, mock_spark_session):
        mock_df = MagicMock()
        mock_read = MagicMock()
        mock_read.format.return_value = mock_read
        mock_read.option.return_value = mock_read
        mock_read.load.return_value = mock_df
        mock_spark_session.builder.getOrCreate.return_value.read = mock_read

        reader = JDBCReader(self.host, self.user, self.password, database=self.database)
        df = reader.read_table(self.table_name)

        self.assertEqual(df, mock_df)


    @patch('spark_jdbc_reader.reader.SparkSession')
    def test_read_table_raises_when_no_database(self, mock_spark_session):
        mock_spark_session.builder.getOrCreate.return_value = MagicMock()
        reader = JDBCReader(self.host, self.user, self.password)
        with self.assertRaises(TableReadError):
            reader.read_table(self.table_name)

    @patch('spark_jdbc_reader.reader.SparkSession')
    def test_read_table_failure_raises_table_read_error(self, mock_spark_session):
        mock_read = MagicMock()
        mock_read.format.return_value = mock_read
        mock_read.option.return_value = mock_read
        mock_read.load.side_effect = Exception("Read error")

        mock_spark_session.builder.getOrCreate.return_value.read = mock_read

        reader = JDBCReader(self.host, self.user, self.password, database=self.database)
        with self.assertRaises(TableReadError) as cm:
            reader.read_table(self.table_name)
        self.assertIn(self.table_name, str(cm.exception))

    @patch('spark_jdbc_reader.reader.SparkSession')
    def test_execute_query_success(self, mock_spark_session):
        mock_df = MagicMock()
        mock_read = MagicMock()
        mock_read.format.return_value = mock_read
        mock_read.option.return_value = mock_read
        mock_read.load.return_value = mock_df
        mock_spark_session.builder.getOrCreate.return_value.read = mock_read

        reader = JDBCReader(self.host, self.user, self.password)
        df = reader.execute_query(self.query)

        self.assertEqual(df, mock_df)


    @patch('spark_jdbc_reader.reader.SparkSession')
    def test_execute_query_failure_raises_query_execution_error(self, mock_spark_session):
        mock_read = MagicMock()
        mock_read.format.return_value = mock_read
        mock_read.option.return_value = mock_read
        mock_read.load.side_effect = Exception("Execution error")

        mock_spark_session.builder.getOrCreate.return_value.read = mock_read

        reader = JDBCReader(self.host, self.user, self.password)
        with self.assertRaises(QueryExecutionError) as cm:
            reader.execute_query(self.query)
        self.assertIn(self.query, str(cm.exception))
        
    def test_build_jdbc_url_with_db(self):
        reader = JDBCReader(self.host, self.user, self.password, port=self.port, database=self.database)
        url = reader._build_jdbc_url()
        expected = f"jdbc:mysql://{self.host}:{self.port}/{self.database}"
        self.assertEqual(url, expected)

    def test_build_jdbc_url_without_db(self):
        reader = JDBCReader(self.host, self.user, self.password, port=self.port)
        url = reader._build_jdbc_url(with_db=False)
        expected = f"jdbc:mysql://{self.host}:{self.port}"
        self.assertEqual(url, expected)


if __name__ == "__main__":
    unittest.main()
