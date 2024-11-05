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


class QuarterlyHires(SQLModel):
    department: str
    job: str
    q1: int
    q2: int
    q3: int
    q4: int


class DepartmentHires(SQLModel):
    id: int
    name: str
    hired_employees: int
