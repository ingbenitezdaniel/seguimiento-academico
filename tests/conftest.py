import pytest

from academic_tracking.student_repository import InMemoryStudentRepository


@pytest.fixture
def repository() -> InMemoryStudentRepository:
    """Return an empty repository for each test."""
    return InMemoryStudentRepository()
