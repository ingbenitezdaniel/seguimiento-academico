import pytest

from academic_tracking.exceptions import StudentNotFoundError
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


def test_service_raises_error_when_student_is_not_found() -> None:
    repository = InMemoryStudentRepository()
    service = StudentService(repository)

    with pytest.raises(StudentNotFoundError, match="Student with id 999 was not found"):
        service.get_student_by_id(999)


def test_service_returns_existing_student_by_id() -> None:
    repository = InMemoryStudentRepository()
    service = StudentService(repository)
    registered_student = service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    found_student = service.get_student_by_id(1)

    assert found_student == registered_student


def test_service_lists_all_students() -> None:
    repository = InMemoryStudentRepository()
    service = StudentService(repository)

    first_student = service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )
    second_student = service.register_student(
        student_id=2,
        first_name="Luis",
        last_name="Perez",
        email="luis.perez@example.com",
    )

    students = service.list_students()

    assert students == [first_student, second_student]


def test_service_returns_empty_list_when_no_students_are_registered() -> None:
    repository = InMemoryStudentRepository()
    service = StudentService(repository)

    students = service.list_students()

    assert students == []
