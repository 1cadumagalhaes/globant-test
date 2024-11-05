import csv
from io import StringIO
from typing import Dict, List

from fastapi.responses import Response


def generate_csv_response(data: List[Dict], filename: str) -> Response:
    """
    Generates a CSV response from a list of dictionaries.

    :param data: List of dictionaries to write into the CSV.
    :param filename: Name of the file to be used in the Content-Disposition.
    :return: FastAPI Response object with CSV data.
    """
    if not data:
        return Response(
            content='',
            media_type='text/csv',
            headers={'Content-Disposition': f'attachment;filename={filename}'},
        )

    # Automatically get fieldnames from the first dictionary
    fieldnames = data[0].keys()
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

    return Response(
        content=output.getvalue(),
        media_type='text/csv',
        headers={'Content-Disposition': f'attachment;filename={filename}'},
    )
