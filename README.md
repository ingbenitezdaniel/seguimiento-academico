# Academic Tracking System

A professional Python project for managing students, courses, enrollments and academic progress.

## Purpose

This project is being developed as part of an advanced Python engineering learning path. Its goal is to apply professional software development practices through a real and progressively evolving system.

## Planned capabilities

* Student and course management
* Enrollment tracking
* Academic progress monitoring
* Data persistence with PostgreSQL
* REST API
* Automated testing
* Docker-based development environment
* Data analysis and future AI capabilities
* Security controls and audit logging

## Engineering practices

* Clean and modular Python code
* Type annotations
* Automated tests with pytest
* Code quality checks
* Git-based version control
* Professional documentation
* Incremental development

## Project status

The student management CLI is implemented with PostgreSQL persistence.

Available commands:

- list
- register
- get
- search
- update
- delete

The CLI provides help without requiring database configuration. Configuration
errors and PostgreSQL operational errors are reported through stderr with exit code 1.

Automated tests, Ruff lint and formatting checks, and strict Mypy type checking
are included in the development workflow.

Course management, enrollment tracking, a REST API, and the other planned
capabilities are not implemented yet.

## Requirements

- Python 3.12 or later
- Git
- Docker Engine with Docker Compose plugin

The following commands assume Bash on Linux and must be run from the project
root directory

## Development installation

Clone the repository and enter its directory:

```bash
git clone https://github.com/ingbenitezdaniel/seguimiento-academico.git
cd seguimiento-academico
```

Create and activate a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install the project and its development dependencies:

```bash
python -m pip install -e ".[dev]"
```

The editable installation makes source code changes available without
reinstalling the package. The dev extra installs the testing and code quality
tools.

Activate the virtual environment in each new terminal session before running
the CLI or development tools.

## Environment configuration

Create your local configuration file:

```bash
cp .env.example .env
```

Edit `.env` and replace the example password with your own local password.

The default development settings are:

| Variable          | Default example value                |
|-------------------|--------------------------------------|
| POSTGRES_HOST     | 127.0.0.1                            |
| POSTGRES_PORT     | 55432                                |
| POSTGRES_DB       | academic_tracking                    |
| POSTGRES_USER     | academic_user                        |
| POSTGRES_PASSWORD | replace-with-your-own-local-password |

The application loads `.env` with python-dotenv. Existing environment variables
take precedence over values in the file.

Docker Compose uses these variables to configure the PostgreSQL container.
The default host port 55432 maps to PostgreSQL port 5432 inside the container.

Keep `.env` local and do not commit credentials to version control.

Changing POSTGRES_DB, POSTGRES_USER, or POSTGRES_PASSWORD does not reconfigure
a database that has already been initialized in the persistent Docker volume.

## PostgreSQL setup

Start the database service:

```bash
docker compose up -d db
```

Check its status:

```bash
docker compose ps
```

Wait until the database service is healthy before continuing.

Apply the student schema to the development database:

```bash
docker compose exec -T db sh -c 'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/schema.sql'
```

The schema uses CREATE TABLE IF NOT EXISTS. This command creates the students
table when missing and preserves an existing table and its data.

On a fresh PostgreSQL volume, the initialization scripts also create
academic_tracking_test and apply the student schema to it.

Initialization scripts run only when PostgreSQL initializes an empty data
directory. They are not rerun when an existing volume is reused.

Stop the services when you finish:

```bash
docker compose stop
```

Stopping the services preserves the database volume and its data.

## CLI usage

Activate the virtual environment and keep PostgreSQL running when executing
student commands. Help does not require database configuration or a connection.

Show general help:

```bash
academic-tracking --help
```

Show help for a specific command:

```bash
academic-tracking register --help
```

The following example uses student ID 1001. Choose an unused ID if that student
already exists. Run the commands in order.

Register a student:

```bash
academic-tracking register --id 1001 --first-name Ana --last-name Garcia --email ana.garcia@example.com
```

List all students:

```bash
academic-tracking list
```

Get the student by ID:

```bash
academic-tracking get --id 1001
```

Search by last name:

```bash
academic-tracking search --last-name Garcia
```

Update the student:

```bash
academic-tracking update --id 1001 --first-name Ana --last-name Garcia --email ana.updated@example.com
```

Delete example student:

```bash
academic-tracking delete --id 1001
```

Registration, update, and deletion commands modify the development database.
The update command requires all student fields.

Student output uses this format:

```text
1001 | Ana Garcia | ana.garcia@example.com
```

Empty lists and searches display:

```text
No students found.
```

### Exit codes

| Codes | Meaning                                                        |
|-------|----------------------------------------------------------------|
| 0     | Successful command or help request                             |
| 1     | Handled domain, configuration, or PostgreSQL operational error |
| 2     | Invalid command-line arguments reported by argparse            |

Handled error messages are written to stderr. Other PostgreSQL error types
are not currently handled by the CLI and may display a traceback.

Handled PostgreSQL operational errors are also logged to stderr at ERROR level.
Log output includes the logger name and the exception traceback to support
diagnosis. Logs are not saved to a file.

## Tests and code quality

Install the development dependencies and activate the virtual environment
before running these commands.

### Automated tests

The full test suite requires PostgreSQL to be running and the
academic_tracking_test database to contain the students table.

Tests use the configured host, port, user, and password, but always select
academic_tracking_test as the database name.

Run the full suite:

```bash
python -m pytest -q
```

Run only the CLI tests, which simulate database access and do not require
a running PostgreSQL server:

```bash
python -m pytest -q tests/test_cli.py
```

PostgreSQL test fixtures roll back changes and close their connections after
each test.

### Code quality checks

Check lint rules:

```bash
python -m ruff check .
```

Check formatting without changing files:

```bash
python -m ruff format --check .
```

Check types:

```bash
python -m mypy src tests
```

To apply formatting when needed:

```bash
python -m ruff format .
```

## Current limitations

- Schema changes are not managed through a migration tool.
- CLI database error handling currently covers psycopg.OperationalError.
- Course, enrollment, and academic progress features are still planned.
