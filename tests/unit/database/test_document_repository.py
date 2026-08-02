import sqlite3
from pathlib import Path

import pytest

from finance_statement_hub.database.connection import create_connection
from finance_statement_hub.database.document_repository import (
    DocumentRepository,
)
from finance_statement_hub.database.schema import initialize_database
from finance_statement_hub.ingestion.models import DocumentCandidate


@pytest.fixture
def connection(tmp_path: Path) -> sqlite3.Connection:
    database_path = tmp_path / "test.sqlite3"

    connection = create_connection(database_path)
    initialize_database(connection)

    yield connection

    connection.close()


def create_document(
    *,
    path: Path,
    sha256: str = "abc123",
) -> DocumentCandidate:
    return DocumentCandidate(
        path=path,
        file_name=path.name,
        extension=".pdf",
        size_bytes=100,
        sha256=sha256,
    )


def test_add_stores_document(
    connection: sqlite3.Connection,
    tmp_path: Path,
) -> None:
    repository = DocumentRepository(connection)
    document = create_document(path=tmp_path / "statement.pdf")

    document_id = repository.add(document)

    row = connection.execute(
        """
        SELECT *
        FROM documents
        WHERE id = ?
        """,
        (document_id,),
    ).fetchone()

    assert row is not None
    assert row["file_name"] == "statement.pdf"
    assert row["sha256"] == "abc123"
    assert row["status"] == "discovered"


def test_exists_by_sha256_returns_true_for_existing_document(
    connection: sqlite3.Connection,
    tmp_path: Path,
) -> None:
    repository = DocumentRepository(connection)
    document = create_document(path=tmp_path / "statement.pdf")

    repository.add(document)

    assert repository.exists_by_sha256("abc123") is True


def test_exists_by_sha256_returns_false_for_unknown_document(
    connection: sqlite3.Connection,
) -> None:
    repository = DocumentRepository(connection)

    assert repository.exists_by_sha256("missing") is False


def test_sha256_must_be_unique(
    connection: sqlite3.Connection,
    tmp_path: Path,
) -> None:
    repository = DocumentRepository(connection)

    first = create_document(
        path=tmp_path / "first.pdf",
        sha256="same-hash",
    )
    second = create_document(
        path=tmp_path / "renamed.pdf",
        sha256="same-hash",
    )

    repository.add(first)

    with pytest.raises(sqlite3.IntegrityError):
        repository.add(second)
