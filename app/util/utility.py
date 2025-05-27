# app/util/utility


# config
from app.config.logger_config import setup_logger
# models
from app.models.response import ResponseEntity
from app.models.exceptions import *
from app.models.enums import HUMAN_READABLE_PARAMS
# helpers
import functools
# type hints
from typing import Any, TYPE_CHECKING


if TYPE_CHECKING:
    from flask import Request

LOGGER = setup_logger("GENERAL UTILITY")


class Utility:
    """
    A utility class providing common methods.

    Methods:

    """

    @staticmethod
    def exception_handler():
        """
        Decorator to handle exceptions and return appropriate responses.
        """

        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    # Execute the wrapped function
                    response = func(*args, **kwargs)

                except DatabaseException as database_exception:
                    LOGGER.error(f"Caught Error. Database error occurred)")
                    LOGGER.error({str(database_exception)})
                    return ResponseEntity.internal_server_error(database_exception.message)

                except MissingInputParameterException as missing_input_exception:
                    LOGGER.error(f"Caught Error. Missing Input Param error occurred)")
                    LOGGER.error({str(missing_input_exception)})
                    return ResponseEntity.bad_request_error(missing_input_exception.message)

                except NotFoundException as not_found_exception:
                    LOGGER.error(f"Caught Error. Not Found error occurred)")
                    LOGGER.error({str(not_found_exception)})
                    return ResponseEntity.not_found_error(str(not_found_exception))

                except PersonAlreadyExistException as person_exists_exception:
                    LOGGER.error(f"Caught Error. Person already exists error occurred)")
                    LOGGER.error({str(person_exists_exception)})
                    return ResponseEntity.bad_request_error(person_exists_exception.message)

                except Exception as e:
                    LOGGER.error(f"Caught Error. An unexpected error) occurred")
                    LOGGER.error({str(e)})
                    return ResponseEntity.internal_server_error(str(e))

                return response

            return wrapper

        return decorator

    @staticmethod
    def retrieve_data(request_data: "Request") -> dict[str, Any]:
        """
        Retrieve data from a Flask request, handling both JSON and form-encoded data.

        Args:
            request_data (Request): The Flask request object.

        Returns:
            dict: The data extracted from the request.
        """
        data = {}

        if not request_data:
            return data
        # Check if request is json
        if request_data.is_json:
            # Handle JSON data
            data = request_data.get_json()
        elif request_data.method == "POST":
            # Handle form data
            data = request_data.form.to_dict()
        elif request_data.method == "GET":
            data = request_data.args.to_dict()

        return data

    @staticmethod
    def get_params_to_human_readable_params_dict(*params: str) -> dict[str, str]:
        """
        Returns a dictionary of parameter passed to human-readable form.
        See HUMAN_READABLE_PARAMETERS in enums.py
        """
        return HUMAN_READABLE_PARAMS.get_readable_dict(*params)

    @staticmethod
    def verify_not_missing_param_in_request(request: dict[str, Any], params_dict: dict[str, str]) -> None:
        """
        Verify if a parameter is missing in the request data.

        Args:
            request (dict): The Flask request object in form of dictionary.
            params_dict (dict): The parameters in the request data that are required
                                where params_dict[key] is human-readable param.

        Returns:
            None

        Raises:
            MissingInputParameterException
        """
        for key in params_dict.keys():
            if request.get(key) is None:
                raise MissingInputParameterException(message=params_dict[key] + " is missing!")

    @staticmethod
    def verify_request_and_get_data(request: "Request", *params_needed: str) -> tuple[Any, ...]:
        request_dict = Utility.retrieve_data(request)  # gets dict of params to value
        params_to_readable_dict = Utility.get_params_to_human_readable_params_dict(*params_needed)
        # gets dict of params to readable strings
        Utility.verify_not_missing_param_in_request(request_dict,
                                                    params_to_readable_dict)  # verifies params are not missing
        return tuple(request_dict.get(key) for key in request_dict.keys())

    @staticmethod
    def assert_not_null(*args) -> bool:
        """
        Check if any of the provided arguments are None. If instance of tuple
        then check every element in it

        Args:
            *args: arguments to be checked

        Returns:
            bool: True if any argument is None, False otherwise.
        """
        for arg in args:
            if isinstance(arg, tuple):
                for elem in arg:
                    if elem is None:
                        return True
            elif arg is None:
                return True

        return False

    @staticmethod
    def assert_not_blank(*args) -> bool:
        """
        Check if any of the provided arguments are empty or whitespace-only strings.

        Args:
            *args: arguments to be checked.

        Returns:
            bool: True if any argument is an empty or whitespace-only string, False otherwise.
        """
        for arg in args:
            if isinstance(arg, str) and not arg.strip():
                return True
        return False

    @staticmethod
    def assert_not_null_then_blank(*args) -> bool:
        """
        Check if any of the provided arguments are None or blank strings.

        Args:
            *args: arguments to be checked.

        Returns:
            bool: True if any argument is None or a blank string, False otherwise.
        """
        return Utility.assert_not_null(*args) or Utility.assert_not_blank(*args)
