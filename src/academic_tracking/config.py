import os
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class DatabaseSettings:
    """Store database connection settings."""

    host: str
    port: int
    dbname: str
    user: str
    password: str

    @classmethod
    def from_environment(cls) -> Self:
        """Build database settings from environment variables."""
        password = os.getenv("POSTGRES_PASSWORD")
        if not password:
            raise RuntimeError("Set POSTGRES_PASSWORD before starting the application")

        return cls(
            host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
            port=int(os.getenv("POSTGRES_PORT", "55432")),
            dbname=os.getenv("POSTGRES_DB", "academic_tracking"),
            user=os.getenv("POSTGRES_USER", "academic_user"),
            password=password,
        )
