FROM python:3.12.2-alpine AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR $PYSETUP_PATH
COPY pyproject.toml ./
RUN uv sync --no-cache

FROM python-base AS production

COPY --from=python-base $VENV_PATH $VENV_PATH
COPY ./app  /api/app
COPY ./pyproject.toml  /api/pyproject.toml

WORKDIR /api
EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]