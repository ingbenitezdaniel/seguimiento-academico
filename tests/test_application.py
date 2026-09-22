import pytest

from academic_tracking.application import open_student_service
from academic_tracking.config import DatabaseSettings
from academic_tracking.exceptions import StudentNotFoundError


def test_application_composes_postgres_student_service(
    postgres_settings: DatabaseSettings,
) -> None:
    with open_student_service(postgres_settings) as service:
        registered_student = service.register_student(
            student_id=1001,
            first_name="Ana",
            last_name="Garcia",
            email="ana.garcia@example.com",
        )

        found_student = service.get_student_by_id(1001)

        assert found_student == registered_student

        service.delete_student(1001)


def test_application_commits_successful_operations(
    postgres_settings: DatabaseSettings,
) -> None:
    with open_student_service(postgres_settings) as service:
        registered_student = service.register_student(
            student_id=1001,
            first_name="Ana",
            last_name="Garcia",
            email="ana.garcia@example.com",
        )

    with open_student_service(postgres_settings) as service:
        found_student = service.get_student_by_id(1001)

        assert found_student == registered_student

        service.delete_student(1001)


def test_application_rolls_back_failed_operations(
    postgres_settings: DatabaseSettings,
) -> None:
    with pytest.raises(RuntimeError, match="Forced application failure"):
        with open_student_service(postgres_settings) as service:
            service.register_student(
                student_id=1002,
                first_name="Luis",
                last_name="Perez",
                email="luis.perez@example.com",
            )

            raise RuntimeError("Forced application failure")

    with open_student_service(postgres_settings) as service:
        with pytest.raises(
            StudentNotFoundError,
            match="Student with id 1002 was not found",
        ):
            service.get_student_by_id(1002)
