from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.connection import (
    get_db,
)
from app.models.responses import DepartmentHires, QuarterlyHires
from app.services.db_service import DBService
from app.utils.parsers import generate_csv_response

router = APIRouter(prefix='/reports', tags=['reports'])


@router.get('/quarterly-hiring-2021', response_model=List[QuarterlyHires])
async def get_quarterly_hiring_2021(
    session: Annotated[AsyncSession, Depends(get_db)],
    format: str = Query(
        'json', enum=['json', 'csv'], description='Response format'
    ),
) -> List[QuarterlyHires]:
    """
    Get a report of employees hired in 2021 by quarter, department and job
    """
    try:
        db_service = DBService(session)
        query = """
        WITH DATA AS (
            SELECT
                d.name AS department,
                j.name AS job,
                datetime
            FROM
                hiredemployees e
            INNER JOIN
                departments d ON department_id = d.id
            INNER JOIN
                jobs j ON department_id = j.id
            WHERE
                e.datetime IS NOT NULL
                AND EXTRACT(year FROM e.datetime) = 2021
        )
        SELECT
            department,
            job,
            SUM(CASE WHEN EXTRACT(quarter FROM datetime) = 1 THEN 1 ELSE 0 END) as q1,
            SUM(CASE WHEN EXTRACT(quarter FROM datetime) = 2 THEN 1 ELSE 0 END) as q2,
            SUM(CASE WHEN EXTRACT(quarter FROM datetime) = 3 THEN 1 ELSE 0 END) as q3,
            SUM(CASE WHEN EXTRACT(quarter FROM datetime) = 4 THEN 1 ELSE 0 END) as q4
        FROM DATA
        GROUP BY
            department,
            job
        ORDER BY
            department,
            job
        """  # noqa: E501
        results = await db_service.execute_select(query)

        if format == 'csv':
            return generate_csv_response(results, 'quarterly_hiring_2021.csv')
        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Error generating quarterly hiring report: {str(e)}',
        ) from e


@router.get(
    '/departments-above-mean-2021', response_model=List[DepartmentHires]
)
async def get_departments_above_mean_2021(
    session: Annotated[AsyncSession, Depends(get_db)],
    format: str = Query(
        'json', enum=['json', 'csv'], description='Response format'
    ),
) -> List[DepartmentHires]:
    """
    Get departments that hired more employees than the mean in 2021
    """
    try:
        db_service = DBService(session)
        query = """
        WITH department_hires AS (
            SELECT
                d.id,
                d.name,
                COUNT(*) as hired_count
            FROM
                hiredemployees e
            INNER JOIN
                departments d ON d.id = e.department_id
            WHERE
                EXTRACT(year FROM e.datetime) = 2021
            GROUP BY
                d.id, d.name
        )
        SELECT
            id,
            name,
            hired_count as hired_employees
        FROM
            department_hires
        WHERE
            hired_count > (SELECT AVG(hired_count) as mean_hired
            FROM department_hires)
        ORDER BY
            hired_count DESC
        """
        results = await db_service.execute_select(query)

        if format == 'csv':
            return generate_csv_response(
                results, 'departments_above_mean_2021.csv'
            )
        return results

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Error generating departments above mean report: {str(e)}',
        ) from e
