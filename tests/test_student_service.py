import pytest

from academic_tracking.exceptions import StudentNotFoundError
from academic_tracking.student import Student
from academic_tracking.student_repository import InMemoryStudentRepository
from academic_tracking.student_service import StudentService


@pytest.fixture
def service(
    repository: InMemoryStudentRepository,
) -> StudentService:
    """Return a service connected to the test repository."""
    return StudentService(repository)


def test_service_registers_student(
    repository: InMemoryStudentRepository,
    service: StudentService,
) -> None:
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


def test_service_rejects_invalid_student_data(
    repository: InMemoryStudentRepository,
    service: StudentService,
) -> None:
    with pytest.raises(ValueError, match="First name cannot be empty"):
        service.register_student(
            student_id=1,
            first_name="   ",
            last_name="Garcia",
            email="ana.garcia",
        )

        assert repository.find_all() == []


def test_service_rejects_duplicate_student_id(
    repository: InMemoryStudentRepository,
    service: StudentService,
) -> None:
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


def test_service_raises_error_when_student_is_not_found(
    repository: InMemoryStudentRepository,
    service: StudentService,
) -> None:
    with pytest.raises(StudentNotFoundError, match="Student with id 999 was not found"):
        service.get_student_by_id(999)


def test_service_returns_existing_student_by_id(
    repository: InMemoryStudentRepository,
    service: StudentService,
) -> None:
    registered_student = service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    found_student = service.get_student_by_id(1)

    assert found_student == registered_student


def test_service_lists_all_students(
    repository: InMemoryStudentRepository,
    service: StudentService,
) -> None:
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


def test_service_returns_empty_list_when_no_students_are_registered(
    repository: InMemoryStudentRepository,
    service: StudentService,
) -> None:
    students = service.list_students()

    assert students == []


def test_service_updates_existing_student(
    repository: InMemoryStudentRepository,
    service: StudentService,
) -> None:
    service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    updated_student = service.update_student(
        student_id=1,
        first_name="Ana Maria",
        last_name="Garcia",
        email="ana.maria.garcia@example.com",
    )

    assert updated_student == Student(
        student_id=1,
        first_name="Ana Maria",
        last_name="Garcia",
        email="ana.maria.garcia@example.com",
    )
    assert repository.find_by_id(1) == updated_student


def test_service_rejects_update_for_nonexistent_student(
    repository: InMemoryStudentRepository,
    service: StudentService,
) -> None:
    with pytest.raises(StudentNotFoundError, match="Student with id 999 was not found"):
        service.update_student(
            student_id=999,
            first_name="Ana",
            last_name="Garcia",
            email="ana.garcia@example.com",
        )

    assert repository.find_all() == []


def test_service_preserves_student_when_update_data_is_invalid(
    repository: InMemoryStudentRepository,
    service: StudentService,
) -> None:
    original_student = service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    with pytest.raises(ValueError, match="Email address is invalid"):
        service.update_student(
            student_id=1,
            first_name="Ana",
            last_name="Garcia",
            email="invalid-email",
        )

    assert repository.find_by_id(1) == original_student


def test_service_deletes_existing_student(
    repository: InMemoryStudentRepository,
    service: StudentService,
) -> None:
    service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    service.delete_student(1)

    assert repository.find_by_id(1) is None
    assert service.list_students() == []


def test_service_rejects_delete_for_nonexistent_student(
    repository: InMemoryStudentRepository,
    service: StudentService,
) -> None:
    with pytest.raises(
        StudentNotFoundError,
        match="Student with id 999 was not found",
    ):
        service.delete_student(999)

    assert repository.find_all() == []
