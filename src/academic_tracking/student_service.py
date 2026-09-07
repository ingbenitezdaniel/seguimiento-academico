from academic_tracking.student import Student
from academic_tracking.student_repository import StudentRepository


class StudentService:
    """Coordinate student-related use cases."""

    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    def register_student(
        self,
        student_id: int,
        first_name: str,
        last_name: str,
        email: str,
    ) -> Student:
        """Create, save, and return a student."""
        student = Student(
            student_id=student_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        self._repository.save(student)

        return student
