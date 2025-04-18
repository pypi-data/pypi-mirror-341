from setuptools import setup, find_packages

setup(
    name='spark-jdbc-reader',
    version='1.0.0',
    description='A lightweight JDBC table and query reader for PySpark.',
    author='Adhi',
    author_email='adhiyaman1705@gmail.com',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'pyspark>=3.0.0'
    ],
    python_requires='>=3.7',
)
