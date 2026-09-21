import os
from collections.abc import Iterator
from typing import Any

import psycopg
import pytest
from dotenv import load_dotenv
from psycopg import Connection

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
def postgres_connection() -> Iterator[Connection[Any]]:
    """Provide a Postgres connection and roll back test changes."""
    load_dotenv()
    password = os.getenv("POSTGRES_PASSWORD")
    if not password:
        raise RuntimeError("Set POSTGRES_PASSWORD in .env before running tests")

    connection = psycopg.connect(
        host="127.0.0.1",
        port=55432,
        dbname="academic_tracking_test",
        user="academic_user",
        password=password,
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
