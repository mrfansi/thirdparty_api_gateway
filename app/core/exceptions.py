class ApplicationException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ValidationException(ApplicationException):
    pass

class NotFoundException(ApplicationException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)

class UnauthorizedException(ApplicationException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)

class ThirdPartyAPIException(ApplicationException):
    def __init__(self, message: str, status_code: int = 500, raw_error: Exception = None):
        super().__init__(message, status_code)
        self.raw_error = raw_error
