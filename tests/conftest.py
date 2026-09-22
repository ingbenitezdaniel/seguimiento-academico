from collections.abc import Iterator
from dataclasses import replace
from typing import Any

import psycopg
import pytest
from dotenv import load_dotenv
from psycopg import Connection

from academic_tracking.config import DatabaseSettings
from academic_tracking.postgres_student_repository import (
    PostgresStudentRepository,
)
from academic_tracking.student_repository import InMemoryStudentRepository
from academic_tracking.student_service import StudentService


@pytest.fixture
def repository() -> InMemoryStudentRepository:
    """Return an empty repository for each test."""
    return InMemoryStudentRepository()


@pytest.fixture
def postgres_settings() -> DatabaseSettings:
    """Return PostgreSQL settings for the test database."""
    load_dotenv()
    return replace(
        DatabaseSettings.from_environment(),
        dbname="academic_tracking_test",
    )


@pytest.fixture
def postgres_connection(
    postgres_settings: DatabaseSettings,
) -> Iterator[Connection[Any]]:
    """Provide a Postgres connection and roll back test changes."""
    connection = psycopg.connect(
        host=postgres_settings.host,
        port=postgres_settings.port,
        dbname=postgres_settings.dbname,
        user=postgres_settings.user,
        password=postgres_settings.password,
    )

    try:
        yield connection
    finally:
        connection.rollback()
        connection.close()


@pytest.fixture
def postgres_repository(
    postgres_connection: Connection[Any],
) -> PostgresStudentRepository:
    """Return a Postgres repository for each test."""
    return PostgresStudentRepository(postgres_connection)


@pytest.fixture
def postgres_service(
    postgres_repository: PostgresStudentRepository,
) -> StudentService:
    """Return a student service backed by PostgreSQL."""
    return StudentService(postgres_repository)
