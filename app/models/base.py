from datetime import datetime
from typing import List, Optional

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)

    @field_validator('id')
    def parse_id(cls, value):
        if isinstance(value, str):
            return int(value)
        return value


class Jobs(BaseModel, SQLModel, table=True):
    name: str
    hired_employees: List['HiredEmployees'] = Relationship(
        back_populates='job'
    )


class Departments(BaseModel, SQLModel, table=True):
    name: str
    hired_employees: List['HiredEmployees'] = Relationship(
        back_populates='department'
    )


class HiredEmployees(BaseModel, SQLModel, table=True):
    name: str
    datetime: datetime
    department_id: int = Field(foreign_key='departments.id')
    job_id: int = Field(foreign_key='jobs.id')

    department: Optional[Departments] = Relationship(
        back_populates='hired_employees'
    )
    job: Optional[Jobs] = Relationship(back_populates='hired_employees')

    @field_validator('datetime')
    def parse_datetime(cls, value):
        if isinstance(value, datetime):
            return value.replace(tzinfo=None)
        try:
            dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
            return dt
        except (ValueError, TypeError):
            raise ValueError(
                'Invalid datetime format. Expected: YYYY-MM-DDThh:mm:ssZ'
            )
