class BaseCustomException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class NotFound(BaseCustomException): ...


class AlreadyExists(BaseCustomException): ...


class NotNullViolationError(BaseCustomException): ...
