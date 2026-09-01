from dataclasses import dataclass


@dataclass(slots=True)
class Student:
    """Represents a student in the academic tracking system."""

    student_id: int
    first_name: str
    last_name: str
    email: str

    def __post_init__(self) -> None:
        """Validate the student after initialization."""
        if not self.first_name.strip():
            raise ValueError("First name cannot be empty")

        if not self.last_name.strip():
            raise ValueError("Last name cannot be empty")

        email = self.email.strip()

        if email.count("@") != 1:
            raise ValueError("Email address is invalid")

        local_part, domain = email.split("@")

        if (
            not local_part
            or "." not in domain
            or domain.startswith(".")
            or domain.endswith(".")
        ):
            raise ValueError("Email address is invalid")

    @property
    def full_name(self) -> str:
        """Return the full name of the student."""
        return f"{self.first_name} {self.last_name}"
