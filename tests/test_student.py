import pytest

from academic_tracking.student import Student


def test_student_returns_full_name() -> None:
    student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    assert student.full_name == "Ana Garcia"


def test_student_rejects_empty_first_name() -> None:
    with pytest.raises(ValueError, match="First name cannot be empty"):
        Student(
            student_id=1,
            first_name="   ",
            last_name="Garcia",
            email="ana.garcia@example.com",
        )


def test_student_rejects_empty_last_name() -> None:
    with pytest.raises(ValueError, match="Last name cannot be empty"):
        Student(
            student_id=1,
            first_name="Ana",
            last_name="\t",
            email="ana.garcia@example.com",
        )


@pytest.mark.parametrize(
    "invalid_email",
    [
        "",
        "ana.garcia",
        "@example.com",
        "ana.garcia@",
        "ana.garcia@example",
        "ana@@example.com",
    ],
)
def test_student_rejects_invalid_email(invalid_email: str) -> None:
    with pytest.raises(ValueError, match="Email address is invalid"):
        Student(
            student_id=1,
            first_name="Ana",
            last_name="Garcia",
            email=invalid_email,
        )
