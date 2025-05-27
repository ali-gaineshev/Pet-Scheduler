# app/models/family.py

# date
from datetime import datetime
# type hints
from typing import Dict, List


class Person:
    """
    Represents a person with an ID, name, and email.

    Attributes:
        person_id (int or None): The unique identifier for the person.
        name (str): The name of the person.
        email (str): The email address of the person (unique)
    """

    PERSON_ID = "person_id"
    NAME = "name"
    EMAIL = "email"
    PASSWORD = "password"

    def __init__(self, name: str, email: str):
        self.person_id: int | None = None
        self.name: str = name
        self.email: str = email

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_person_id(self):
        return self.person_id

    def set_person_id(self, person_id: int):
        self.person_id = person_id

    def __str__(self):
        return f"Person Id: {self.person_id}\nName: {self.name}\nEmail: {self.email}"

    def to_dict(self) -> Dict[str, str]:
        """
        Converts the Person instance to a dictionary.

        Returns:
            dict: A dictionary with the person's name and email.
        """
        data = {}
        if self.name:
            data["name"] = self.name

        if self.email:
            data["email"] = self.email

        return data


class Family:
    """
    Represents a family consisting of multiple persons.

    Attributes:
        family_id (int or None): The unique identifier for the family.
        members (list[Person]): A list of Person instances representing family members.
        head_member_id (int or None): The unique identifier of the head member.
    """

    def __init__(self, members: List[Person]):
        """
        Initializes a new Family instance.

        Args:
            members (list[Person]): A list of Person instances representing family members.
        """
        self.family_id = None
        self.members: List[Person] = members  # a list of member objects
        self.head_member_id: int | None = None if len(members) == 0 else self.members[0].get_person_id()  # admin role

    def add_member(self, new_member: Person) -> None:
        """
        Adds a new member to the family.

        Args:
            new_member (Person): The new Person instance to be added to the family.
        """
        self.members.append(new_member)


class Task:
    """
    Represents a task with a description, date, and assignment details.

    Attributes:
        task_id (int or None): The unique identifier for the task.
        description (str): The task description.
        date (str): The date and time of the task in 'yyyy-mm-dd hh:min:sec' format.
        completed (bool): Whether the task is completed.
        person_id_to_do (int or None): The ID of the person assigned to do the task.
    """

    def __init__(self, description: str, date: datetime):
        """
        Initializes a new Task instance.

        Args:
            description (str): The task description.
            date (str): The date and time of the task in 'yyyy-mm-dd hh:min:sec' format.
        """
        self.task_id = None
        self.description = description  # the task string
        self.date = date  # yyyy-mm-dd hh:min:sec
        self.completed = False
        self.person_id_to_do = None

    def assign_task(self, person_id):
        self.person_id_to_do = person_id

    def set_completed(self, completed):
        self.completed = completed

    def set_id(self, task_id):
        self.task_id = task_id

    def set_date(self, date):
        self.date = date

    def set_task_description(self, description):
        self.description = description

    def set_task_id(self, task_id):
        self.task_id = task_id

    def get_task_description(self):
        return self.description

    def get_date(self):
        return self.date
    
    def is_completed(self):
        return self.completed

    def get_person_id(self):
        return self.person_id_to_do

    def __str__(self):
        return f"Id - {self.task_id}. What to do: {self.description}. Date: {self.date}"
