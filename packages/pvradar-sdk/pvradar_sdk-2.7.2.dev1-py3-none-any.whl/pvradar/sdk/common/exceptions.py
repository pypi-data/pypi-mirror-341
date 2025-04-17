from typing import Union
from httpx import Response


class ApiException(Exception):
    status_code: int
    response: Union[(Response, None)]

    def __init__(self, status_code: int, message: str, response: Union[(Response, None)] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class ClientException(Exception):
    response: Union[(Response, None)]

    def __init__(self, message: str, response: Union[(Response, None)] = None):
        super().__init__(message)
        self.response = response


class PvradarSdkException(RuntimeError):
    pass
