from contextlib import nullcontext

import pytest

from academic_tracking import cli
from academic_tracking.cli import run_cli
from academic_tracking.config import DatabaseSettings
from academic_tracking.student import Student
from academic_tracking.student_repository import InMemoryStudentRepository
from academic_tracking.student_service import StudentService


def test_cli_lists_students(
    repository: InMemoryStudentRepository,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StudentService(repository)
    service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )
    service.register_student(
        student_id=2,
        first_name="Juan",
        last_name="Perez",
        email="juan.perez@example.com",
    )

    exit_code = run_cli(service, ["list"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == (
        "1 | Ana Garcia | ana.garcia@example.com\n"
        "2 | Juan Perez | juan.perez@example.com\n"
    )


def test_cli_reports_when_there_are_no_students(
    repository: InMemoryStudentRepository,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StudentService(repository)

    exit_code = run_cli(service, ["list"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "No students found.\n"


def test_cli_register_student(
    repository: InMemoryStudentRepository,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StudentService(repository)

    exit_code = run_cli(
        service,
        [
            "register",
            "--id",
            "1",
            "--first-name",
            "Ana",
            "--last-name",
            "Garcia",
            "--email",
            "ana.garcia@example.com",
        ],
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Student 1 registered.\n"
    assert service.get_student_by_id(1) == Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )


def test_cli_gets_student_by_id(
    repository: InMemoryStudentRepository,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StudentService(repository)
    service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    exit_code = run_cli(service, ["get", "--id", "1"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "1 | Ana Garcia | ana.garcia@example.com\n"


def test_cli_reports_when_student_is_not_found(
    repository: InMemoryStudentRepository,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StudentService(repository)

    exit_code = run_cli(service, ["get", "--id", "999"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == "Student with id 999 was not found\n"


def test_cli_searches_students_by_last_name(
    repository: InMemoryStudentRepository,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StudentService(repository)
    service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )
    service.register_student(
        student_id=2,
        first_name="Juan",
        last_name="Garcia",
        email="juan.garcia@example.com",
    )
    service.register_student(
        student_id=3,
        first_name="Maria",
        last_name="Perez",
        email="maria.perez@example.com",
    )

    exit_code = run_cli(
        service,
        ["search", "--last-name", "Garcia"],
    )
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == (
        "1 | Ana Garcia | ana.garcia@example.com\n"
        "2 | Juan Garcia | juan.garcia@example.com\n"
    )


def test_cli_reports_when_search_has_no_matches(
    repository: InMemoryStudentRepository,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StudentService(repository)
    service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    exit_code = run_cli(
        service,
        ["search", "--last-name", "Perez"],
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "No students found.\n"


def test_cli_updates_student(
    repository: InMemoryStudentRepository,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StudentService(repository)
    service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    exit_code = run_cli(
        service,
        [
            "update",
            "--id",
            "1",
            "--first-name",
            "Ana",
            "--last-name",
            "Garcia",
            "--email",
            "ana.actualizada@example.com",
        ],
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Student 1 updated.\n"
    assert service.get_student_by_id(1) == Student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.actualizada@example.com",
    )


def test_cli_reports_when_updated_student_is_not_found(
    repository: InMemoryStudentRepository,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StudentService(repository)

    exit_code = run_cli(
        service,
        [
            "update",
            "--id",
            "999",
            "--first-name",
            "Ana",
            "--last-name",
            "Garcia",
            "--email",
            "ana.actualizada@example.com",
        ],
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == "Student with id 999 was not found\n"


def test_cli_deletes_student(
    repository: InMemoryStudentRepository,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StudentService(repository)
    service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    exit_code = run_cli(service, ["delete", "--id", "1"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Student 1 deleted.\n"
    assert captured.err == ""
    assert repository.find_by_id(1) is None


def test_cli_reports_when_deleted_student_is_not_found(
    repository: InMemoryStudentRepository,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StudentService(repository)

    exit_code = run_cli(service, ["delete", "--id", "999"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == "Student with id 999 was not found\n"


def test_cli_reports_duplicate_student_id(
    repository: InMemoryStudentRepository,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StudentService(repository)
    service.register_student(
        student_id=1,
        first_name="Ana",
        last_name="Garcia",
        email="ana.garcia@example.com",
    )

    exit_code = run_cli(
        service,
        [
            "register",
            "--id",
            "1",
            "--first-name",
            "Juan",
            "--last-name",
            "Perez",
            "--email",
            "juan.perez@example.com",
        ],
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == "Student with id 1 already exists\n"


def test_cli_reports_invalid_student_email(
    repository: InMemoryStudentRepository,
    capsys: pytest.CaptureFixture[str],
) -> None:
    service = StudentService(repository)

    exit_code = run_cli(
        service,
        [
            "register",
            "--id",
            "1",
            "--first-name",
            "Ana",
            "--last-name",
            "Garcia",
            "--email",
            "invalid-email",
        ],
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == "Email address is invalid\n"
    assert repository.find_all() == []


def test_main_composes_service_and_runs_cli(
    repository: InMemoryStudentRepository,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    settings = DatabaseSettings(
        host="database.example",
        port=5432,
        dbname="academic_tracking",
        user="academic_user",
        password="test_password",
    )
    service = StudentService(repository)

    monkeypatch.setattr(cli, "load_dotenv", lambda: None)
    monkeypatch.setattr(
        DatabaseSettings,
        "from_environment",
        lambda: settings,
    )

    def open_test_service(
        received_settings: DatabaseSettings,
    ) -> nullcontext[StudentService]:
        assert received_settings == settings
        return nullcontext(service)

    monkeypatch.setattr(cli, "open_student_service", open_test_service)

    exit_code = cli.main(["list"])

    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == "No students found.\n"
    assert captured.err == ""
