import logging
from typing import Sequence, Type, TypeVar

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, select

ModelType = TypeVar('ModelType', bound=SQLModel)

logger = logging.getLogger(__name__)


class DBService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_batch(
        self, records: Sequence[ModelType], batch_size: int = 1000
    ) -> None:
        """
        Create records in batches.

        Args:
            records: Sequence of model instances to create
            batch_size: Number of records to create in each batch
        """
        try:
            # Validate batch size
            if len(records) > batch_size:
                raise ValueError(
                    f'Batch size exceeded: {len(records)} > {batch_size}'
                )

            # Add all records
            self.session.add_all(records)

            # Commit the transaction
            try:
                await self.session.commit()
            except SQLAlchemyError as e:
                await self.session.rollback()
                logger.error(
                    f'Database error during batch creation: {str(e)}',
                    exc_info=True,
                )
                raise

        except ValueError as e:
            logger.error(
                f'Validation error in create_batch: {str(e)}', exc_info=True
            )
            raise
        except Exception as e:
            logger.error(
                f'Unexpected error in create_batch: {str(e)}', exc_info=True
            )
            raise

    async def get_all(self, model: Type[ModelType]) -> list[ModelType]:
        """
        Get all records for a given model.

        Args:
            model: SQLModel class to query

        Returns:
            List of model instances
        """
        result = await self.session.execute(select(model))
        return list(result.scalars().all())

    async def execute_select(
        self, query: str, params: dict | None = None
    ) -> list[dict]:
        """
        Execute a SELECT SQL query and return results.

        Args:
            query: SQL SELECT query string
            params: Optional dictionary of parameters for SQL query

        Returns:
            List of dictionaries containing query results, where each
            dictionary represents a row with column names as keys
        """
        try:
            result = await self.session.execute(text(query), params or {})
            columns = result.keys()
            return [
                dict(zip(columns, row, strict=False))
                for row in result.fetchall()
            ]

        except SQLAlchemyError as e:
            logger.error(
                f'Database error during SELECT execution: {str(e)}',
                exc_info=True,
            )
            raise
        except Exception as e:
            logger.error(
                f'Unexpected error in execute_select: {str(e)}', exc_info=True
            )
            raise
