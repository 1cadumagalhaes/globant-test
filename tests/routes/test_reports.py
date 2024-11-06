from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_quarterly_hiring_2021_json(
    async_client: AsyncClient, populated_async_session
):
    response = await async_client.get('/reports/quarterly-hiring-2021')
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert isinstance(data, list)

    first_record = data[0]
    assert 'department' in first_record
    assert 'job' in first_record
    assert 'q1' in first_record
    assert 'q2' in first_record
    assert 'q3' in first_record
    assert 'q4' in first_record

    engineering_record = next(
        r
        for r in data
        if r['department'] == 'Engineering' and r['job'] == 'Software Engineer'
    )
    assert engineering_record is not None


@pytest.mark.asyncio
async def test_get_departments_above_mean_2021(
    async_client: AsyncClient, populated_async_session
):
    response = await async_client.get('/reports/departments-above-mean-2021')
    assert response.status_code == HTTPStatus.OK
    data = response.json()

    assert isinstance(data, list)
    first_record = data[0]
    assert 'id' in first_record
    assert 'name' in first_record
    assert 'hired_employees' in first_record

    engineering_dept = next(r for r in data if r['name'] == 'Engineering')
    assert engineering_dept['hired_employees'] > 1
