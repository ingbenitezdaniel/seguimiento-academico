import pytest

from academic_tracking.student import Student
from academic_tracking.student_repository import InMemoryStudentRepository
from academic_tracking.student_service import StudentService


def test_service_registers_student() -> None:
    repository = InMemoryStudentRepository()
    service = StudentService(repository)

    student = service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    assert student == Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    assert repository.find_by_id(1) == student


def test_service_rejects_invalid_student_data() -> None:
    repository = InMemoryStudentRepository()
    service = StudentService(repository)

    with pytest.raises(ValueError, match="First name cannot be empty"):
        service.register_student(
            student_id=1,
            first_name="   ",
            last_name="Garcia",
            email="ana.garcia",
        )

        assert repository.find_all() == []


def test_service_rejects_duplicate_student_id() -> None:
    repository = InMemoryStudentRepository()
    service = StudentService(repository)

    first_student = service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    with pytest.raises(ValueError, match="Student with id 1 already exists"):
        service.register_student(
            student_id=1,
            first_name="Luis",
            last_name="Perez",
            email="luis.perez@example.com",
        )

    assert repository.find_by_id(1) == first_student
