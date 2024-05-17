from fastapi import status


class CustomException(Exception):
    def __init__(self, message, error_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(message)
        self.error_code = error_code


class DatabaseException(CustomException):
    pass
