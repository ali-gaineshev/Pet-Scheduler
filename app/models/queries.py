# db/queries.py

# type hints
from typing import Tuple


class Query:
    __PERSONS_TABLE = "PERSONS"
    __TASKS_TABLE = "TASKS"

    @staticmethod
    def insert_new_person(name: str, email: str, hashed_password: str) -> Tuple[str, Tuple[str, str, str]]:
        return (
            f"INSERT INTO {Query.__PERSONS_TABLE} (name, email, password) "
            f"VALUES (%s, %s, %s) RETURNING person_id",
            (name, email, hashed_password)
        )

    @staticmethod
    def select_person_by_id(person_id: int) -> Tuple[str, Tuple[int]]:
        return (
            f"SELECT * FROM {Query.__PERSONS_TABLE} WHERE person_id = %s",
            (person_id,)
        )

    @staticmethod
    def select_person_by_email(email: str) -> Tuple[str, Tuple[str]]:
        return (
            f"SELECT * FROM {Query.__PERSONS_TABLE} WHERE email = %s",
            (email,)
        )

    @staticmethod
    def insert_new_task(description: str, date: str, is_completed: bool, person_id: int)\
            -> Tuple[str, Tuple[str, str, bool, int]]:
        return (
            f"INSERT INTO {Query.__TASKS_TABLE} (description, date, is_completed, person_id)"
            f" VALUES (%s, %s, %s, %s) RETURNING task_id",
            (description, date, is_completed, person_id)
        )

    @staticmethod
    def get_task_by_task_id(task_id: int) -> Tuple[str, Tuple[int]]:
        return (
            f"SELECT * FROM {Query.__TASKS_TABLE} where task_id = %s", (task_id,)
        )
