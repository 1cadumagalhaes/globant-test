import io
import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.connection import get_db
from app.models.base import Departments, HiredEmployees, Jobs
from app.models.responses import UploadResponse
from app.services.csv_service import CSVService
from app.services.db_service import DBService

router = APIRouter(prefix='/upload', tags=['upload'])

logger = logging.getLogger(__name__)


async def process_upload(
    file: UploadFile,
    model_class: type,
    has_headers: bool,
    db: AsyncSession,
    entity_name: str,
) -> UploadResponse:
    """
    Generic function to process CSV uploads for any model.
    """
    try:
        if not file.filename.endswith('.csv'):
            logger.error(
                f'Invalid file type for {entity_name}: {file.filename}'
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='File must be a CSV',
            )

        contents = await file.read()
        csv_file = io.StringIO(contents.decode('utf-8'))

        records, errors = CSVService.read_uploaded_csv(
            csv_file, model_class, has_headers
        )

        if not records and errors:
            logger.error(f'CSV validation failed for {entity_name}: {errors}')
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={'message': 'No valid records found', 'errors': errors},
            )

        try:
            db_service = DBService(db)
            await db_service.create_batch(records)
        except Exception as e:
            logger.error(
                f'Database error while uploading {entity_name}: {str(e)}',
                exc_info=True,
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Database error: {str(e)}',
            )

        logger.info(
            f'Successfully uploaded {len(records)} {entity_name} records'
        )
        return UploadResponse(
            message=f'{entity_name} uploaded successfully',
            total_records=len(records),
            errors=errors,
        )

    except UnicodeDecodeError as e:
        logger.error(
            f'File encoding error for {entity_name}: {str(e)}', exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid CSV file encoding. Please use UTF-8',
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f'Unexpected error processing {entity_name} upload: {str(e)}',
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post('/departments', response_model=UploadResponse)
async def upload_departments(
    file: UploadFile = File(...),
    has_headers: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """Upload departments from CSV file."""
    return await process_upload(
        file, Departments, has_headers, db, 'Departments'
    )


@router.post('/jobs', response_model=UploadResponse)
async def upload_jobs(
    file: UploadFile = File(...),
    has_headers: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """Upload jobs from CSV file."""
    return await process_upload(file, Jobs, has_headers, db, 'Jobs')


@router.post('/employees', response_model=UploadResponse)
async def upload_employees(
    file: UploadFile = File(...),
    has_headers: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """Upload hired employees from CSV file."""
    return await process_upload(
        file, HiredEmployees, has_headers, db, 'Employees'
    )
