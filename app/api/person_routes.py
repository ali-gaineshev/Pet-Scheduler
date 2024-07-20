# app/api/person_routes.py

# flask
from flask import Blueprint
from flask import request
# util
from app.util.db_utility import DatabaseUtility
from app.util.utility import Utility
# logger config
from app.config.logger_config import setup_logger
# Models
from app.models.family import *
from app.models.response import ResponseEntity
from app.models.exceptions import *
from app.models.error_messages import ErrorMessage

person_bp = Blueprint('person_routes', __name__, url_prefix='/api')
LOGGER = setup_logger("PERSON API")


@person_bp.route("/validateLogin", methods=["POST"])
@Utility.exception_handler()
def validate_login():
    email, password = Utility.verify_request_and_get_data(request, Person.EMAIL, Person.PASSWORD)
    person: Person = DatabaseUtility.PersonTransaction.login_with_email(email, password)

    if person is None:
        raise NotFoundException(ErrorMessage.PERSON_DOES_NOT_EXIST_LOGIN)
    LOGGER.debug(f"HERE")
    LOGGER.debug(f"Person: {person}")
    return ResponseEntity.ok(**person.to_dict())

@person_bp.route("/getPersonInfo/", methods=['GET'])
@Utility.exception_handler()
def get_person_info_by_id():
    person_id = Utility.verify_request_and_get_data(request, Person.PERSON_ID)

    person: Person = DatabaseUtility.PersonTransaction.get_person_info_by_id(person_id)
    if not person:
        raise NotFoundException(ErrorMessage.PERSON_DOES_NOT_EXIST)

    return ResponseEntity.ok(**person.to_dict())


@person_bp.route("/insertNewPerson", methods=['POST'])
@Utility.exception_handler()
def insert_person():
    data = Utility.retrieve_data_from_json_or_form_or_args(request)
    name, email, password = Utility.verify_request_and_get_data(request, Person.NAME, Person.EMAIL, Person.PASSWORD)

    p: Person = Person(email=email, name=name)
    person_id = DatabaseUtility.commit_new_person(p, password)
    if not person_id:
        raise NotFoundException(ErrorMessage.PERSON_DOES_NOT_EXIST)

    return ResponseEntity.ok(**{"person_id": person_id})


@person_bp.route("/checkIfPersonExists", methods=['POST'])
@Utility.exception_handler()
def login():
    data = Utility.retrieve_data_from_json_or_form_or_args(request)

    if (not data.get('email')):
        raise MissingInputParameterException(message="Email is missing")
    if (not data.get('password')):
        raise MissingInputParameterException(message="Password is missing")

    email = data.get('email')
    password = data.get('password')

    person: Person = DatabaseUtility.login(email, password)

    if (not person or Utility.assert_not_null_then_blank
        (person.get_email(), person.get_name(), person.get_person_id())):
        return ResponseEntity.error("Wrong login credentials")

    return ResponseEntity.ok(**person.to_dict())
