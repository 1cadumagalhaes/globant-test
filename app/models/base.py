from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class Jobs(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class Departments(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str


class HiredEmployees(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    datetime: datetime
    department_id: int = Field(foreign_key='departments.id')
    job_id: int = Field(foreign_key='jobs.id')

    department: 'Departments' = Relationship(back_populates='departments')
    job: 'Jobs' = Relationship(back_populates='jobs')
