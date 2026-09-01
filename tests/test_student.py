from academic_tracking.student import Student


def test_student_returns_full_name() -> None:
    student = Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    assert student.full_name == "Ana Garcia"
