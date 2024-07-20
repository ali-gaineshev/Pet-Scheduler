# app/util/transactions

# logger
from app.config.logger_config import setup_logger
# exceptions
from app.models.exceptions import DatabaseException
# type hints
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from psycopg2.extensions import cursor

LOGGER = setup_logger("TRANSACTION")


class Transaction:
    """
    This class provides static methods to handle database transactions,
    specifically fetching one or all records from the database.
    """

    @staticmethod
    def request_database_fetchone(conn_cursor: "cursor", query: str, params: tuple, exception_message: str)\
            -> tuple[str, ...]:
        """
        Executes a query to fetch a single record from the database.
        Logs an error and raises a DatabaseException if the query fails.
        """
        try:
            conn_cursor.execute(query, params)
            return conn_cursor.fetchone()
        except Exception as e:
            LOGGER.error(exception_message, e)
            raise DatabaseException(exception_message, e)

    @staticmethod
    def request_database_fetchall(conn_cursor: "cursor", query: str, params: tuple, exception_message: str)\
            -> tuple[str, ...]:
        """
        Executes a query to fetch all records from the database.
        Logs an error and raises a DatabaseException if the query fails.
        """
        try:
            conn_cursor.execute(query, params)
            return conn_cursor.fetchall()
        except Exception as e:
            LOGGER.error(exception_message, e)
            raise DatabaseException(exception_message, e)
