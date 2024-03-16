from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code = 404, detail = detail)

class MyException(Exception):
    def __init__(self, item_id: str):
        self.item_id = item_id