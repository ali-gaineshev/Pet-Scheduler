# app/util/db_utility

# models
from app.models.enums import DB_POSITION
from app.models.family import *
from app.models.exceptions import DatabaseException
from app.models.response_messages import ErrorMessage
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

    SUCCESS = 0

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
        def commit_new_person(cursor, person: Person, password: str) -> None | int:

            hashed_password = Encrypt.hash_password(password)# Store hashed password in db

            query, params = Query.insert_new_person(
                name=person.get_name(),
                email=person.get_email(),
                hashed_password=hashed_password
            )
            info = (Transaction.
                    request_database_fetchone(cursor, query, params, ErrorMessage.ERROR_REGISTERING))

            if info is None:
                LOGGER.debug(f"Error registering new person with email - {person.get_email()}")
                return None

            return DatabaseUtility.SUCCESS

        @staticmethod
        @Connection.get_db_connection()
        def check_if_person_exists(cursor, email: str) -> bool:
            query, params = Query.check_person_exists(email=email)
            person_exists = (Transaction.
                      request_database_fetchone(cursor, query, params, ErrorMessage.GENERAL_ERROR))

            return person_exists if person_exists is not None else False
        
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
