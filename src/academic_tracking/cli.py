import logging
import sys
from argparse import ArgumentParser, Namespace
from collections.abc import Sequence

import psycopg
from dotenv import load_dotenv

from academic_tracking.application import open_student_service
from academic_tracking.config import DatabaseSettings
from academic_tracking.exceptions import StudentNotFoundError
from academic_tracking.student import Student
from academic_tracking.student_service import StudentService

logger = logging.getLogger(__name__)


def _format_student(student: Student) -> str:
    """Format a student for terminal output."""
    return (
        f"{student.student_id} | "
        f"{student.first_name} {student.last_name} | "
        f"{student.email}"
    )


def _print_students(students: Sequence[Student]) -> None:
    """Print students or an empty-result message."""
    if not students:
        print("No students found.")
        return

    for student in students:
        print(_format_student(student))


def _add_student_id_argument(parser: ArgumentParser) -> None:
    """Add student identifier argument to a command parser."""
    parser.add_argument(
        "--id",
        dest="student_id",
        type=int,
        required=True,
    )


def _add_student_arguments(parser: ArgumentParser) -> None:
    """Add all student data arguments to a command parser."""
    _add_student_id_argument(parser)
    parser.add_argument("--first-name", required=True)
    parser.add_argument("--last-name", required=True)
    parser.add_argument("--email", required=True)


def build_parser() -> ArgumentParser:
    """Build the command-line argument parser."""
    parser = ArgumentParser(prog="academic-tracking")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List all students")

    register_parser = subparsers.add_parser(
        "register",
        help="Register a new student",
    )
    _add_student_arguments(register_parser)

    get_parser = subparsers.add_parser(
        "get",
        help="Get a student by identifier",
    )
    _add_student_id_argument(get_parser)

    search_parser = subparsers.add_parser(
        "search",
        help="Search students by last name",
    )
    search_parser.add_argument("--last-name", required=True)

    update_parser = subparsers.add_parser(
        "update",
        help="Update a student",
    )
    _add_student_arguments(update_parser)

    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a student",
    )
    _add_student_id_argument(delete_parser)

    return parser


def run_cli(
    service: StudentService,
    arguments: Sequence[str] | None = None,
) -> int:
    """Run a student command using the provided service."""
    parser = build_parser()
    namespace = parser.parse_args(arguments)
    return _execute_command(service, namespace)


def _execute_command(service: StudentService, namespace: Namespace) -> int:
    """Execute a student command using the parsed arguments."""
    try:
        if namespace.command == "list":
            _print_students(service.list_students())

        elif namespace.command == "register":
            student = service.register_student(
                student_id=namespace.student_id,
                first_name=namespace.first_name,
                last_name=namespace.last_name,
                email=namespace.email,
            )
            print(f"Student {student.student_id} registered.")

        elif namespace.command == "get":
            student = service.get_student_by_id(namespace.student_id)
            print(_format_student(student))

        elif namespace.command == "search":
            students = service.find_students_by_last_name(namespace.last_name)
            _print_students(students)

        elif namespace.command == "update":
            student = service.update_student(
                student_id=namespace.student_id,
                first_name=namespace.first_name,
                last_name=namespace.last_name,
                email=namespace.email,
            )
            print(f"Student {student.student_id} updated.")

        elif namespace.command == "delete":
            service.delete_student(student_id=namespace.student_id)
            print(f"Student {namespace.student_id} deleted.")

    except (StudentNotFoundError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1

    return 0


def main(arguments: Sequence[str] | None = None) -> int:
    """Configure the application and run the command-line interface."""
    parser = build_parser()
    namespace = parser.parse_args(arguments)

    logging.basicConfig(
        level=logging.ERROR,
        format="%(levelname)s | %(name)s | %(message)s",
    )

    load_dotenv()

    try:
        settings = DatabaseSettings.from_environment()
    except (RuntimeError, ValueError) as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 1

    try:
        with open_student_service(settings) as service:
            return _execute_command(service, namespace)
    except psycopg.OperationalError:
        logger.exception("Database operation failed.")
        print(
            "Database error: unable to complete the operation.",
            file=sys.stderr,
        )
        return 1
