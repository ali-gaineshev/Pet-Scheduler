# app/models/enums

from enum import Enum
from typing import Dict

class DB_POSITION(Enum):
    """
    Enum for database positions of the class attributes.
    """
    PERSON_PERSON_ID = 0
    PERSON_NAME = 1
    PERSON_EMAIL = 2
    PERSON_PASSWORD = 3

    TASK_TASK_ID = 0
    TASK_DESCRIPTION = 1
    TASK_DATE = 2
    TASK_IS_COMPLETED = 3
    TASK_PERSON_ID = 4

    FAMILY_FAMILY_ID = 0
    FAMILY_HEAD_MEMBER_ID = 1

    FAMILY_MEMBERS_FAMILY_ID = 0
    FAMILY_MEMBERS_PERSON_ID = 1


class STATUS_CODE(Enum):
    """ Common HTTP codes for response """
    OK = 200
    BAD_REQUEST = 400
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


class HUMAN_READABLE_PARAMS(Enum):
    """ Enum of common parameters and version of them in more human-readable form. """

    PERSON_ID_TUP = ("person_id", "Person ID")
    EMAIL_TUP = ("email", "Email")
    NAME_TUP = ("name", "Name")
    PASSWORD_TUP = ("password", "Password")

    @property
    def param_name(self):
        return self.value[0]

    @property
    def readable(self):
        return self.value[1]

    @classmethod
    def get_readable_dict(cls, *input_params) -> Dict[str, str]:
        params_to_readable = {}
        for input_param_name in input_params:
            for param in cls:
                if param.param_name == input_param_name:
                    params_to_readable[param.param_name] = param.readable
        return params_to_readable
