# app/util/db_utility

# models
from app.models.enums import DB_POSITION
from app.models.family import *
from app.models.exceptions import DatabaseException
from app.models.error_messages import ErrorMessage
# config
from app.config.logger_config import setup_logger
# utility
from app.models.queries import Query
from app.util.utility import Utility
from app.util.db_connection import Connection
from app.util.encrypt import Encrypt
from app.util.transactions import Transaction

# type hints


LOGGER = setup_logger("DB_UTILITY")


class DatabaseUtility:
    """ Database utility functions that execute queries """

    class PersonTransaction:

        @staticmethod
        @Connection.get_db_connection(commit=False)
        def get_person_info_by_id(cursor, person_id: int) -> Person | None:
            """
            Get all the user information based on person id

            Parameters:
            - person_id - (int) PK

            Returns:
            - Person class if user is found
            - NONE if no user exists

            Throws:
            - DatabaseException
            """
            query, params = Query.select_person_by_id(person_id)
            info: tuple = Transaction.request_database_fetchone(cursor, query, params, ErrorMessage.FETCHING_USER_INFO)

            if Utility.assert_not_null(info):
                LOGGER.debug(f"Person by id {person_id} doesn't exist")
                return None

            return Person(info[DB_POSITION.PERSON_NAME.value],
                          info[DB_POSITION.PERSON_EMAIL.value])

        @staticmethod
        @Connection.get_db_connection(commit=False)
        def login_with_email(cursor, email: str, password: str) -> Person | None:
            query, params = Query.select_person_by_email(email)
            info: tuple = (Transaction.
                           request_database_fetchone(cursor, query, params, ErrorMessage.FETCHING_USER_INFO))

            if Utility.assert_not_null(info):
                LOGGER.debug(f"Person by email {email} doesn't exist")
                return None

            person = Person(info[DB_POSITION.PERSON_NAME.value], info[DB_POSITION.PERSON_EMAIL.value])
            person.set_person_id(info[DB_POSITION.PERSON_PERSON_ID.value])

            if Encrypt.match_password(password, info[DB_POSITION.PERSON_PASSWORD.value]):
                return person
            else:
                return None

        @staticmethod
        @Connection.get_db_connection(commit=True)
        def commit_new_person(cursor, person: Person, password: str):
            try:
                name = person.get_name()
                email = person.get_email()

                if Utility.assert_not_null(name, email, password) or Utility.assert_not_blank(name, email, password):
                    raise DatabaseException("One of the input parameters is empty")

                # Store hashed password in db
                hashed_password = Encrypt.hash_password(password)

                query, params = Query.insert_new_person(
                    name=person.get_name(),
                    email=person.get_email(),
                    hashed_password=hashed_password
                )
                cursor.execute(query, params)
                info = cursor.fetchone()

                if Utility.assert_not_null(info):
                    LOGGER.debug(f"Person id for inserting new person was not created")
                    return None

                return info[DB_POSITION.PERSON_PERSON_ID.value]
            except Exception as e:
                LOGGER.error("Error inserting new person: %s", e)
                raise DatabaseException("Error inserting new person", e)

    @staticmethod
    @Connection.get_db_connection(commit=True)
    def commit_new_task(cursor, task: Task):
        query, params = Query.insert_new_task(
            description=task.get_task_description(),
            date=task.get_date(),
            is_completed=task.is_completed(),
            person_id=task.get_person_id()
        )

        cursor.execute(query, params)
        info = cursor.fetchone()

        return info

    @staticmethod
    @Connection.get_db_connection()
    def get_task_by_task_id(cursor, task_id: int):
        query, params = Query.get_task_by_task_id(task_id)
        cursor.execute(query, params)
        info = cursor.fetchone()
        return info
