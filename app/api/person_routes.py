# app/api/person_routes.py

# flask
from flask import Blueprint, request

from app.models.enums import CONSTANTS
# util
from app.util.db_utility import DatabaseUtility
from app.util.utility import Utility
# logger config
from app.config.logger_config import setup_logger
# Models
from app.models.family import *
from app.models.response import ResponseEntity
from app.models.exceptions import *
from app.models.response_messages import *

person_bp = Blueprint('person_routes', __name__, url_prefix='/api')
LOGGER = setup_logger("PERSON API")


@person_bp.route("/validateLogin", methods=["POST"])
@Utility.exception_handler()
def validate_login():
    email, password = Utility.verify_request_and_get_data(request, Person.EMAIL, Person.PASSWORD)
    person: Person = DatabaseUtility.PersonTransaction.login_with_email(email, password)

    if person is None:
        raise NotFoundException(ErrorMessage.PERSON_DOES_NOT_EXIST_LOGIN)

    LOGGER.debug(f"Person logged in:\n{person}")
    return ResponseEntity.ok(**person.to_dict())


@person_bp.route("/registerNewUser", methods=['POST'])
@Utility.exception_handler()
def insert_person():
    name, email, password = (Utility.
                             verify_request_and_get_data(request, Person.NAME, Person.EMAIL, Person.PASSWORD))

    person: Person = Person(email=email, name=name)

    is_success = DatabaseUtility.PersonTransaction.commit_new_person(person, password)
    if is_success != CONSTANTS.SUCCESS_OPERATION.value:
        raise PersonAlreadyExistException(ErrorMessage.PERSON_ALREADY_EXISTS)

    return ResponseEntity.ok(**{"alert_message": OkMessage.SUCCESS})


@person_bp.route("/getPersonInfo/", methods=['GET'])
@Utility.exception_handler()
def get_person_info_by_id():
    person_id = Utility.verify_request_and_get_data(request, Person.PERSON_ID)

    person: Person = DatabaseUtility.PersonTransaction.get_person_info_by_id(person_id)
    if not person:
        raise NotFoundException(ErrorMessage.PERSON_DOES_NOT_EXIST)

    return ResponseEntity.ok(**person.to_dict())
