class MessageAppExceptionBase(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class RestableErrorBase(MessageAppExceptionBase):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code

    def to_json(self) -> dict:
        return {
            "message": self.message,
            "status_code": self.status_code
        }
