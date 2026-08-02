import sqlite3
from pathlib import Path


def create_connection(database_path: Path) -> sqlite3.Connection:
    """Create a configured SQLite database connection."""
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")
    return connection
