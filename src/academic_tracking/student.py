from dataclasses import dataclass


@dataclass(slots=True)
class Student:
    """Represents a student in the academic tracking system."""

    student_id: int
    first_name: str
    last_name: str
    email: str

    @property
    def full_name(self) -> str:
        """Return the full name of the student."""
        return f"{self.first_name} {self.last_name}"
