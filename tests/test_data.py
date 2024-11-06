import datetime
from typing import List

from app.models.base import Departments, HiredEmployees, Jobs


def create_test_departments() -> List[Departments]:
    return [
        Departments(id=1, name='Engineering'),
        Departments(id=2, name='Marketing'),
        Departments(id=3, name='Sales'),
        Departments(id=4, name='Human Resources'),
    ]


def create_test_jobs() -> List[Jobs]:
    return [
        Jobs(id=1, name='Software Engineer'),
        Jobs(id=2, name='Marketing Specialist'),
        Jobs(id=3, name='Sales Representative'),
        Jobs(id=4, name='HR Manager'),
    ]


def create_test_employees() -> List[HiredEmployees]:
    return [
        HiredEmployees(
            id=1,
            name='John Doe',
            datetime=datetime.datetime(2021, 1, 15),
            department_id=1,
            job_id=1,
        ),
        HiredEmployees(
            id=2,
            name='Jane Smith',
            datetime=datetime.datetime(2021, 2, 1),
            department_id=1,
            job_id=1,
        ),
        HiredEmployees(
            id=3,
            name='Bob Johnson',
            datetime=datetime.datetime(2021, 3, 10),
            department_id=2,
            job_id=2,
        ),
        HiredEmployees(
            id=4,
            name='Alice Brown',
            datetime=datetime.datetime(2021, 4, 5),
            department_id=3,
            job_id=3,
        ),
        HiredEmployees(
            id=5,
            name='Charlie Wilson',
            datetime=datetime.datetime(2021, 6, 15),
            department_id=1,
            job_id=1,
        ),
        HiredEmployees(
            id=6,
            name='Diana Miller',
            datetime=datetime.datetime(2021, 9, 1),
            department_id=2,
            job_id=2,
        ),
        HiredEmployees(
            id=7,
            name='Edward Davis',
            datetime=datetime.datetime(2021, 12, 10),
            department_id=3,
            job_id=3,
        ),
    ]
