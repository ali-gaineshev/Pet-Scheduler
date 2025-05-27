from flask import jsonify
from app.models.enums import STATUS_CODE


class ResponseEntity:
    """ Response Entity that generates a JSON response with code """

    @staticmethod
    def ok(**kwargs):
        """
        Returns a JSON response with a 200 OK status.

        Args:
            kwargs: Additional key-value pairs to include in the response.

        Returns:
            A tuple containing a JSON response and HTTP status code 200.
        """
        response = {"message": "ok"}
        response.update(kwargs)
        return jsonify(response), STATUS_CODE.OK.value

    @staticmethod
    def general_error(error_message: str, code: STATUS_CODE):
        """
        Returns a JSON response with an error message and the given status code.

        Args:
            error_message (str): Description of the error.
            code (STATUS_CODE): HTTP status code to return.

        Returns:
            A tuple containing a JSON response and the given HTTP status code.
        """
        return jsonify({"message": "error", "error_message": error_message}), code.value

    @staticmethod
    def error(error_message: str):
        """
        Returns a JSON response with a 200 status. Meaning request is handled but input data is wrong.

        Args:
            error_message (str): Description of the error.

        Returns:
            A tuple containing a JSON response and HTTP status code 200.
        """
        return ResponseEntity.general_error(error_message, STATUS_CODE.OK)

    @staticmethod
    def internal_server_error(error_message: str):
        """
        Returns a JSON response with a 500 Internal Server Error status.

        Args:
            error_message (str): Description of the error.

        Returns:
            A tuple containing a JSON response and HTTP status code 500.
        """
        return ResponseEntity.general_error(error_message, STATUS_CODE.INTERNAL_SERVER_ERROR)

    @staticmethod
    def bad_request_error(error_message: str):
        """
        Returns a JSON response with a 400 Bad Request status.

        Args:
            error_message (str): Description of the error.

        Returns:
            A tuple containing a JSON response and HTTP status code 400.
        """
        return ResponseEntity.general_error(error_message, STATUS_CODE.BAD_REQUEST)

    @staticmethod
    def forbidden_error(error_message: str):
        """
        Returns a JSON response with a 403 Forbidden status.

        Args:
            error_message (str): Description of the error.

        Returns:
            A tuple containing a JSON response and HTTP status code 403.
        """
        return ResponseEntity.general_error(error_message, STATUS_CODE.FORBIDDEN)

    @staticmethod
    def not_found_error(error_message: str):
        """
        Returns a JSON response with a 404 Not Found status.

        Args:
            error_message (str): Description of the error.

        Returns:
            A tuple containing a JSON response and HTTP status code 404.
        """
        return ResponseEntity.general_error(error_message, STATUS_CODE.NOT_FOUND)

    @staticmethod
    def unsupported_media_type_error(error_message: str):
        """
        Returns a JSON response with a 412 Unsupported Media Type status.

        Args:
            error_message (str): Description of the error.

        Returns:
            A tuple containing a JSON response and HTTP status code 412.
        """
        return ResponseEntity.general_error(error_message, STATUS_CODE.UNSUPPORTED_MEDIA_TYPE)
