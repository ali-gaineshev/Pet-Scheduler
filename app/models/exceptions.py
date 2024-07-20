# app/models/exceptions

class DatabaseException(Exception):
    """Exception raised for errors that occur during database operations.

    Attributes:
        message (str): The error message describing the exception.
        exception (Exception, optional): The inner exception, if any, that caused this exception.
    """

    def __init__(self, message: str, exception=None):
        super().__init__(message)
        self.message = message
        self.exception = exception

    def get_exception_message(self):
        return str(self.exception) if self.exception else "No inner exception"

    def __str__(self):
        if self.exception:
            return f"{self.message}\n{self.exception}"
        return self.message


class MissingInputParameterException(Exception):
    """Exception raised when a required input parameter is missing.

    Attributes:
        message (str): The error message describing the exception.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundException(Exception):
    """Exception raised when a requested resource is not found.

    Attributes:
        message (str): The error message describing the exception.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
