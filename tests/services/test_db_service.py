import pytest

from app.models.base import Departments, HiredEmployees
from app.services.db_service import DBService
from tests.test_data import (
    create_test_departments,
    create_test_employees,
    create_test_jobs,
)


@pytest.mark.asyncio
async def test_create_batch(async_session):
    db_service = DBService(async_session)
    departments = create_test_departments()
    await db_service.create_batch(departments)

    result = await db_service.get_all(Departments)
    assert len(result) == 4  # noqa: PLR2004


@pytest.mark.asyncio
async def test_execute_select_with_data(async_session):
    db_service = DBService(async_session)

    query = 'SELECT * FROM departments WHERE name LIKE :name'
    results = await db_service.execute_select(query, {'name': 'Engineering'})

    assert len(results) == 1
    assert results[0]['name'] == 'Engineering'


@pytest.mark.asyncio
async def test_get_all_with_relationships(async_session):
    db_service = DBService(async_session)

    jobs = create_test_jobs()
    employees = create_test_employees()

    await db_service.create_batch(jobs)
    await db_service.create_batch(employees)
    all_employees = await db_service.get_all(HiredEmployees)
    assert len(all_employees) == 7  # noqa: PLR2004
