from collections.abc import Iterator
from contextlib import contextmanager

import psycopg

from academic_tracking.config import DatabaseSettings
from academic_tracking.postgres_student_repository import (
    PostgresStudentRepository,
)
from academic_tracking.student_service import StudentService


@contextmanager
def open_student_service(
    settings: DatabaseSettings,
) -> Iterator[StudentService]:
    """Open a PostgreSQL-backed student service."""
    with psycopg.connect(
        host=settings.host,
        port=settings.port,
        dbname=settings.dbname,
        user=settings.user,
        password=settings.password,
    ) as connection:
        repository = PostgresStudentRepository(connection)
        yield StudentService(repository)
