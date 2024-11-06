import csv
import io
from typing import List, Tuple, Type, TypeVar

from sqlmodel import SQLModel
from sqlmodel import inspect as sqlmodel_inspect

ModelType = TypeVar('ModelType', bound=SQLModel)


class CSVService:
    @staticmethod
    def read_uploaded_csv(
        file: io.StringIO,
        model_class: Type[ModelType],
        has_headers: bool = False,
    ) -> Tuple[List[ModelType], List[Tuple[int, str]]]:
        records: List[ModelType] = []
        errors: List[Tuple[int, str]] = []

        try:
            reader = csv.reader(file)
            if has_headers:
                next(reader)

            mapper = sqlmodel_inspect(model_class)
            expected_fields = [column.description for column in mapper.columns]

            for row_number, row in enumerate(reader, start=1):
                try:
                    if len(row) != len(expected_fields):
                        errors.append((
                            row_number,
                            f'Expected {len(expected_fields)} columns '
                            f'({", ".join(expected_fields)}), '
                            f'got {len(row)}',
                        ))
                        continue

                    record_dict = CSVService._convert_row_to_dict(
                        row, expected_fields, mapper
                    )

                    record = model_class.model_validate(record_dict)
                    records.append(record)

                except ValueError as e:
                    errors.append((row_number, f'Value error: {str(e)}'))
                except Exception as e:
                    errors.append((row_number, f'Unexpected error: {str(e)}'))

        except Exception as e:
            errors.append((0, f'File reading error: {str(e)}'))

        return records, errors

    @staticmethod
    def _convert_row_to_dict(
        row: List[str],
        expected_fields: List[str],
        mapper,
    ) -> dict:
        record_dict = {}
        for field, value in zip(expected_fields, row, strict=False):
            record_dict[field] = value
        return record_dict
