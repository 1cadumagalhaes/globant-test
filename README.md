# Globant FastAPI application

## Tech Stack

- Backend: FastAPI, SQLModel, Asyncpg
- Database: PostgreSQL
- ORM: SQLModel
- Migration: Alembic
- Testing: Pytest
- Package Manager: uv
- Development: Docker, Docker Compose

## Project Structure

```sh
.
├── .postgres-data/
├── app/
│   ├── database/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── utils/
├── migrations/
├── tests/
│   ├── routes/
│   └── services/
├── Dockerfile
├── compose.yaml
├── alembic.ini
├── pyproject.toml
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- uv package manager

### Installation/development

1. Clone the repository:

   ```sh
   git clone https://github.com/1cadumagalhaes/globant-test
   cd globant-test
   ```

2. Install uv if you haven't already:

   ```sh
   pip install uv
   ```

3. Install dependencies:

   ```sh
   uv sync
   ```

### Running the Application

#### Using Docker

Start the application and its dependencies:

- *Obs*: If there is no `.postgres-data` directory, create it before running the application. We choose to let its path set so this can be easily implemented in production.

```sh
docker compose up
```

For development with auto-reload:

```sh
docker compose up --build --watch
```

#### Using Taskipy

Start the application and its dependencies:

- *Obs*: This requires the installation of dependencies with `uv sync`.

```sh
task docker-up
```

For development with auto-reload:

```sh
task docker-dev
```

Stop the application:

```sh
task docker-down
```

Check the logs:

```sh
task docker-logs
```

#### Local Development

1. Start the development server:

   ```sh
   task dev
   ```

### Testing

Run tests:

```sh
task test
```

Generate coverage report:

```sh
task post_test
```

### Code Quality

Lint the code:

```sh
task lint
```

Format the code:

```sh
task format
```

Run all checks (lint, format, test):

```sh
task check
```

### Other commands

Clean project directory:

```sh
task clean
```

Create postgres-data folder

```sh
task init
```

## Documentation

API documentation is available at `/docs` when the server is running
