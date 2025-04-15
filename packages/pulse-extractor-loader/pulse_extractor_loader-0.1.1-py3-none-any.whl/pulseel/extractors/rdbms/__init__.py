import logging

import polars as pl




def test_connection(conn_str: str):
    """
    Tests the database connection to ensure that the given connection string is valid
    and can be used to interact with the database. Attempts to execute a simple
    query to confirm connectivity.

    :param conn_str: The database connection string used to establish a connection.
    :type conn_str: str
    :return: None
    :raises Exception: If the database connection cannot be established or the tests
        query fails.
    """
    try:
        logging.info("Testing database connection...")
        pl.read_database_uri("SELECT 1", conn_str)
        logging.info("Connection successful!")
    except Exception as e:
        logging.error("Connection failed!")
        raise e

