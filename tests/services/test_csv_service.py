import pytest
from io import StringIO
from app.services.csv_service import CSVService
from app.models.base import Departments, Jobs, HiredEmployees


@pytest.fixture
def valid_departments_csv():
    return StringIO('1,IT Department\n2,HR Department')


@pytest.fixture
def invalid_departments_csv():
    return StringIO('1\n2')


def test_read_valid_departments_csv(valid_departments_csv):
    records, errors = CSVService.read_uploaded_csv(
        valid_departments_csv, Departments
    )
    assert len(records) == 2
    assert len(errors) == 0
    assert records[0].name == 'IT Department'


def test_read_invalid_departments_csv(invalid_departments_csv):
    records, errors = CSVService.read_uploaded_csv(
        invalid_departments_csv, Departments
    )
    assert len(records) == 0
    assert len(errors) > 0
