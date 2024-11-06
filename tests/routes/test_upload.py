from http import HTTPStatus
from io import BytesIO

import pytest
from httpx import AsyncClient


@pytest.fixture
def departments_csv():
    return BytesIO(b'1,Engineering\n2,Marketing\n3,Sales\n4,Human Resources')


@pytest.fixture
def jobs_csv():
    return BytesIO(
        b'10,Software Engineer\n2,Marketing Specialist\n'
        b'11,Sales Representative\n4,HR Manager'
    )


@pytest.fixture
def employees_csv():
    return BytesIO(
        b'1,John Doe,2021-01-15 00:00:00,1,10\n'
        b'2,Jane Smith,2021-02-01 00:00:00,1,10\n'
        b'3,Bob Johnson,2021-03-10 00:00:00,2,11'
    )


@pytest.mark.asyncio
async def test_upload_departments_success(
    async_client: AsyncClient, departments_csv
):
    files = {'file': ('departments.csv', departments_csv, 'text/csv')}
    response = await async_client.post('/upload/departments', files=files)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['total_records'] == 4  # noqa: PLR2004
    assert len(data['errors']) == 0


@pytest.mark.asyncio
async def test_upload_jobs_success(async_client: AsyncClient, jobs_csv):
    files = {'file': ('jobs.csv', jobs_csv, 'text/csv')}
    response = await async_client.post('/upload/jobs', files=files)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['total_records'] == 4  # noqa: PLR2004
    assert len(data['errors']) == 0


@pytest.mark.asyncio
async def test_upload_employees_success(
    async_client: AsyncClient,
    employees_csv,
):
    # Then upload employees
    files = {'file': ('employees.csv', employees_csv, 'text/csv')}
    response = await async_client.post('/upload/employees', files=files)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['total_records'] == 3  # noqa: PLR2004
    assert len(data['errors']) == 0


@pytest.mark.asyncio
async def test_upload_invalid_csv_format(async_client: AsyncClient):
    invalid_csv = BytesIO(b'invalid,data\nwithout,proper,columns')
    files = {'file': ('test.csv', invalid_csv, 'text/csv')}
    response = await async_client.post('/upload/departments', files=files)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    data = response.json()
    print(data)
    assert 'errors' in data['detail']


@pytest.mark.asyncio
async def test_upload_non_csv_file(async_client: AsyncClient):
    files = {'file': ('test.txt', BytesIO(b'not a csv'), 'text/plain')}
    response = await async_client.post('/upload/departments', files=files)
    assert response.status_code == HTTPStatus.BAD_REQUEST
