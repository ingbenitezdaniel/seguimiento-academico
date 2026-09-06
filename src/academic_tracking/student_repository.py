from academic_tracking.student import Student


class InMemoryStudentRepository:
    """Store student in memory."""

    def __init__(self) -> None:
        self._students: dict[int, Student] = {}

    def save(self, student: Student) -> None:
        """Save a student using their identifier."""
        if student.student_id in self._students:
            raise ValueError(f"Student with id {student.student_id} already exists")

        self._students[student.student_id] = student

    def find_by_id(self, student_id: int) -> Student | None:
        """Find a student by its identifier."""
        return self._students.get(student_id)

    def find_all(self) -> list[Student]:
        """Return all students in insertion order."""
        return list(self._students.values())

    def find_by_last_name(self, last_name: str) -> list[Student]:
        """Find students by last name."""
        return [
            student
            for student in self._students.values()
            if student.last_name == last_name
        ]
