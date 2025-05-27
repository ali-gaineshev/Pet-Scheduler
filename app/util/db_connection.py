# app/util/db_connection

# postgres connector
import psycopg2
# helpers
import os
import functools
# flask
from flask import g
# config
from app.config.logger_config import setup_logger
from dotenv import load_dotenv, find_dotenv
# models
from app.models.exceptions import DatabaseException
# type hints
from typing import Dict

LOGGER = setup_logger("CONNECTION")


class Connection:
    """ class that connects to the database """

    @staticmethod
    def __read_credentials() -> Dict[str, str]:
        """
        READ DB credentials from secret file!

        Returns:
            dict: credentials
        """
        dotenv_path = find_dotenv()  # return path to .env file
        load_dotenv(dotenv_path)

        dbname = os.getenv('DB_NAME')
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')

        return {'dbname': dbname, 'user': user, 'password': password, 'host': host, 'port': port}

    @staticmethod
    def get_db():
        try:
            if not hasattr(g, 'db'):
                g.db = psycopg2.connect(**Connection.__read_credentials())
                LOGGER.info("Database is connected")
        except Exception as e:
            LOGGER.error("Couldn't connect to the database! Something went wrong either with the server, username or "
                         + "password.\n" + str(e))
            return None

        return g.db

    @staticmethod
    def close_db(e=None):
        if e is not None:
            LOGGER.error(f"Error with closing the db:\n{str(e)}")
            return

        db = g.pop('db', None)

        if db is not None:
            db.close()

    @staticmethod
    def get_db_connection(commit: bool = False):
        """
        Decorator. Gets the connection to db. If connected, proceed to original function
        Otherwise raises an Exception or rollsback
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                conn = Connection.get_db()
                if conn is None:
                    LOGGER.error("No connection to the db\n")
                    raise DatabaseException("Database is not up")
                try:
                    with conn.cursor() as cursor:
                        result = func(cursor, *args, **kwargs)
                        if commit:
                            conn.commit()  # Commit the transaction
                        return result
                except Exception as e:
                    conn.rollback()  # Rollback in case of error
                    LOGGER.critical(f"Error with conn to db:\n{e}")
                    return None

            return wrapper

        return decorator
