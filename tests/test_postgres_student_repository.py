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
from academic_tracking.student import Student
from academic_tracking.student_repository import StudentRepository


@pytest.fixture
def postgres_connection() -> Iterator[Connection[Any]]:
    """Provide a PostgreSQL connection and roll back test changes."""
    load_dotenv()
    password = os.getenv("POSTGRES_PASSWORD")
    if not password:
        raise RuntimeError("Set POSTGRES_PASSWORD in .env before running this test")

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
    return PostgresStudentRepository(postgres_connection)


def test_postgres_repository_saves_and_finds_student_by_id(
    postgres_repository: PostgresStudentRepository,
) -> None:
    student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    postgres_repository.save(student)

    assert postgres_repository.find_by_id(1) == student


def test_postgres_returns_none_when_student_does_not_exist(
    postgres_repository: PostgresStudentRepository,
) -> None:
    found_student = postgres_repository.find_by_id(999)

    assert found_student is None


def test_postgres_repository_rejects_duplicate_student_id(
    postgres_repository: PostgresStudentRepository,
) -> None:
    first_student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )
    duplicate_student = Student(
        student_id=1,
        first_name="Luis",
        last_name="Perez",
        email="luis.perez@example.com",
    )
    postgres_repository.save(first_student)

    with pytest.raises(ValueError, match="Student with id 1 already exists"):
        postgres_repository.save(duplicate_student)

    assert postgres_repository.find_by_id(1) == first_student


def test_postgres_repository_returns_all_students(
    postgres_repository: PostgresStudentRepository,
) -> None:
    first_student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )
    second_student = Student(
        student_id=2,
        first_name="Luis",
        last_name="Perez",
        email="luis.perez@example.com",
    )
    postgres_repository.save(first_student)
    postgres_repository.save(second_student)

    students = postgres_repository.find_all()

    assert students == [first_student, second_student]


def test_postgres_finds_students_by_last_name(
    postgres_repository: PostgresStudentRepository,
) -> None:
    ana = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )
    juan = Student(
        student_id=2,
        first_name="Juan",
        last_name="Garcia",
        email="juan.garcia@example.com",
    )
    maria = Student(
        student_id=3,
        first_name="Maria",
        last_name="Perez",
        email="maria.perez@example.com",
    )
    postgres_repository.save(ana)
    postgres_repository.save(juan)
    postgres_repository.save(maria)

    found_students = postgres_repository.find_by_last_name("Garcia")

    assert found_students == [ana, juan]


def test_postgres_repository_returns_empty_list_when_last_name_is_not_found(
    postgres_repository: PostgresStudentRepository,
) -> None:
    student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )
    postgres_repository.save(student)

    found_students = postgres_repository.find_by_last_name("Benitez")

    assert found_students == []


def test_postgres_repository_updates_existing_student(
    postgres_repository: PostgresStudentRepository,
) -> None:
    original_student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )
    update_student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )
    postgres_repository.save(original_student)

    postgres_repository.update(update_student)

    assert postgres_repository.find_by_id(1) == update_student


def test_postgres_repository_rejects_update_for_nonexistent_student(
    postgres_repository: PostgresStudentRepository,
) -> None:
    student = Student(
        student_id=999,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    with pytest.raises(ValueError, match="Student with id 999 does not exist"):
        postgres_repository.update(student)

    assert postgres_repository.find_all() == []


def test_postgres_repository_deletes_existing_student(
    postgres_repository: PostgresStudentRepository,
) -> None:
    student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )
    postgres_repository.save(student)

    postgres_repository.delete(1)

    assert postgres_repository.find_by_id(1) is None
    assert postgres_repository.find_all() == []


def test_postgres_repository_rejects_delete_for_nonexistent_student(
    postgres_repository: PostgresStudentRepository,
) -> None:
    with pytest.raises(
        ValueError,
        match="Student with id 999 does not exist",
    ):
        postgres_repository.delete(999)

    assert postgres_repository.find_all() == []


def test_postgres_repository_satisfies_protocol(
    postgres_repository: PostgresStudentRepository,
) -> None:
    student_repository: StudentRepository = postgres_repository

    assert student_repository.find_all() == []
