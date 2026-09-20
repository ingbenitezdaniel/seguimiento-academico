from typing import Any

from psycopg import Connection
from psycopg.errors import UniqueViolation

from academic_tracking.student import Student


class PostgresStudentRepository:
    """Store students in PostgreSQL."""

    def __init__(self, connection: Connection[Any]) -> None:
        self._connection = connection

    def save(self, student: Student) -> None:
        """Save a student."""
        self._connection.execute("SAVEPOINT save_student")

        try:
            self._connection.execute(
                """
                INSERT INTO students (
                    student_id,
                    first_name,
                    last_name,
                    email
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    student.student_id,
                    student.first_name,
                    student.last_name,
                    student.email,
                ),
            )
        except UniqueViolation as error:
            self._connection.execute("ROLLBACK TO SAVEPOINT save_student")
            self._connection.execute("RELEASE SAVEPOINT save_student")
            raise ValueError(
                f"Student with id {student.student_id} already exists"
            ) from error
        else:
            self._connection.execute("RELEASE SAVEPOINT save_student")

    def find_by_id(self, student_id: int) -> Student | None:
        """Find a student by its identifier."""
        cursor = self._connection.execute(
            """
            SELECT student_id, first_name, last_name, email
            FROM students
            WHERE student_id = %s
            """,
            (student_id,),
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return Student(
            student_id=row[0],
            first_name=row[1],
            last_name=row[2],
            email=row[3],
        )

    def find_all(self) -> list[Student]:
        """Return all students ordered by identifier."""
        cursor = self._connection.execute(
            """
            SELECT student_id, first_name, last_name, email
            FROM students
            ORDER BY student_id
            """
        )
        rows = cursor.fetchall()

        return [
            Student(
                student_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
            )
            for row in rows
        ]

    def find_by_last_name(self, last_name: str) -> list[Student]:
        """Find students by last name."""
        cursor = self._connection.execute(
            """
            SELECT student_id, first_name, last_name, email
            FROM students
            WHERE last_name = %s
            ORDER BY student_id
            """,
            (last_name,),
        )
        rows = cursor.fetchall()

        return [
            Student(
                student_id=row[0],
                first_name=row[1],
                last_name=row[2],
                email=row[3],
            )
            for row in rows
        ]

    def update(self, student: Student) -> None:
        """Update an existing student."""
        cursor = self._connection.execute(
            """
            UPDATE students
            SET first_name = %s, last_name = %s, email = %s
            WHERE student_id = %s
            """,
            (
                student.first_name,
                student.last_name,
                student.email,
                student.student_id,
            ),
        )

        if cursor.rowcount == 0:
            raise ValueError(f"Student with id {student.student_id} does not exist")

    def delete(self, student_id: int) -> None:
        """Delete an existing student."""
        cursor = self._connection.execute(
            """
            DELETE FROM students WHERE student_id = %s
            """,
            (student_id,),
        )

        if cursor.rowcount == 0:
            raise ValueError(f"Student with id {student_id} does not exist")
