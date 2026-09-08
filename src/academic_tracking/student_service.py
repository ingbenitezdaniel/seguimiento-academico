from academic_tracking.exceptions import StudentNotFoundError
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

    def get_student_by_id(self, student_id: int) -> Student:
        """Return a student by identifier."""
        student = self._repository.find_by_id(student_id)

        if student is None:
            raise StudentNotFoundError(f"Student with id {student_id} was not found")

        return student

    def list_students(self) -> list[Student]:
        """Return all registered students."""
        return self._repository.find_all()

    def update_student(
        self,
        student_id: int,
        first_name: str,
        last_name: str,
        email: str,
    ) -> Student:
        """Update and return an existing student."""
        self.get_student_by_id(student_id)

        updated_student = Student(
            student_id=student_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        self._repository.update(updated_student)

        return updated_student
