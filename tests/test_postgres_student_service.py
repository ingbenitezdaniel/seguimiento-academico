from academic_tracking.student_service import StudentService


def test_student_service_registers_and_retrieves_student_using_postgres(
    postgres_service: StudentService,
) -> None:
    registered_student = postgres_service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    found_student = postgres_service.get_student_by_id(1)

    assert found_student == registered_student
