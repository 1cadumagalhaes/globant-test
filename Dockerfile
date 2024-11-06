FROM python:3.12.2-alpine AS builder

RUN apk add --no-cache gcc

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    UV_PROJECT_ENVIRONMENT=/usr/local \
    PATH="/root/.local/bin:$PATH" \
    PYTHONPATH="/usr/local/lib/python3.12/site-packages:$PYTHONPATH"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /api
COPY pyproject.toml ./
RUN uv tool install alembic && uv tool install uvicorn && uv sync --no-cache --no-dev

FROM python:3.12.2-alpine AS production

RUN apk add --no-cache coreutils \
    && rm -rf /var/cache/apk/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local \
    PATH="/root/.local/bin:$PATH" \
    PYTHONPATH="/usr/local/lib/python3.12/site-packages:$PYTHONPATH"

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

WORKDIR /api
COPY ./app  /api/app
COPY ./alembic.ini  /api/alembic.ini
COPY ./migrations  /api/migrations
COPY ./pyproject.toml  /api/pyproject.toml

EXPOSE 8000
CMD uv tool run alembic upgrade head && uv tool run uvicorn app.main:app --host 0.0.0.0 --port 8000