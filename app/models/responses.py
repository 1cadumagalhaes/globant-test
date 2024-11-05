from typing import List

from sqlmodel import SQLModel


class Message(SQLModel):
    message: str


class ErrorDetail(SQLModel):
    row: int
    message: str


class UploadResponse(SQLModel):
    message: str
    total_records: int
    errors: List[ErrorDetail] = []
