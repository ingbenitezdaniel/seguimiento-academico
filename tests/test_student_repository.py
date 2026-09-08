import pytest

from academic_tracking.student import Student
from academic_tracking.student_repository import (
    InMemoryStudentRepository,
    StudentRepository,
)


def test_repository_saves_and_finds_student_by_id() -> None:
    repository = InMemoryStudentRepository()
    student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    repository.save(student)

    found_student = repository.find_by_id(1)

    assert found_student == student


def test_repository_returns_none_when_student_does_not_exist() -> None:
    repository = InMemoryStudentRepository()

    found_student = repository.find_by_id(999)

    assert found_student is None


def test_repository_rejects_duplicate_student_id() -> None:
    repository = InMemoryStudentRepository()
    first_student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )
    duplicate_student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    repository.save(first_student)

    with pytest.raises(ValueError, match="Student with id 1 already exists"):
        repository.save(duplicate_student)

    assert repository.find_by_id(1) == first_student


def test_repository_returns_all_students() -> None:
    repository = InMemoryStudentRepository()
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

    repository.save(first_student)
    repository.save(second_student)

    students = repository.find_all()

    assert students == [first_student, second_student]


def test_repository_find_all_returns_independent_list() -> None:
    repository = InMemoryStudentRepository()
    student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )
    repository.save(student)

    students = repository.find_all()
    students.clear()

    assert repository.find_all() == [student]


def test_repository_finds_students_by_last_name() -> None:
    repository = InMemoryStudentRepository()
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

    repository.save(ana)
    repository.save(juan)
    repository.save(maria)

    found_students = repository.find_by_last_name("Garcia")

    assert found_students == [ana, juan]


def test_repository_empty_list_when_last_name_is_not_found() -> None:
    repository = InMemoryStudentRepository()
    student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )
    repository.save(student)

    found_students = repository.find_by_last_name("Benitez")

    assert found_students == []


def test_in_memory_repository_satisfies_protocol() -> None:
    repository: StudentRepository = InMemoryStudentRepository()
    student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    repository.save(student)

    assert repository.find_by_id(1) == student


def test_repository_rejects_update_for_nonexistent_student() -> None:
    repository: StudentRepository = InMemoryStudentRepository()
    student = Student(
        student_id=999,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    with pytest.raises(ValueError, match="Student with id 999 does not exist"):
        repository.update(student)

    assert repository.find_all() == []
