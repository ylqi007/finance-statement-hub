import sqlite3
from pathlib import Path

import pytest

from finance_statement_hub.database import (
    DocumentRepository,
    create_connection,
    initialize_database,
)
from finance_statement_hub.ingestion import IngestionOutcome
from finance_statement_hub.ingestion.service import ingest_documents


@pytest.fixture
def connection(tmp_path: Path) -> sqlite3.Connection:
    connection = create_connection(tmp_path / "test.sqlite3")
    initialize_database(connection)

    yield connection

    connection.close()


def test_ingest_documents_registers_new_document(
    connection: sqlite3.Connection,
    tmp_path: Path,
) -> None:
    inbox_path = tmp_path / "inbox"
    inbox_path.mkdir()

    statement_path = inbox_path / "statement.pdf"
    statement_path.write_bytes(b"synthetic statement")

    repository = DocumentRepository(connection)

    results = ingest_documents(inbox_path, repository)

    assert len(results) == 1
    assert results[0].outcome is IngestionOutcome.IMPORTED
    assert results[0].document_id is not None
    assert results[0].document.file_name == "statement.pdf"

    row = connection.execute(
        """
        SELECT *
        FROM documents
        """
    ).fetchone()

    assert row is not None
    assert row["file_name"] == "statement.pdf"


def test_ingest_documents_skips_previously_registered_document(
    connection: sqlite3.Connection,
    tmp_path: Path,
) -> None:
    inbox_path = tmp_path / "inbox"
    inbox_path.mkdir()

    statement_path = inbox_path / "statement.pdf"
    statement_path.write_bytes(b"synthetic statement")

    repository = DocumentRepository(connection)

    first_results = ingest_documents(inbox_path, repository)
    second_results = ingest_documents(inbox_path, repository)

    print("first_results = {}", first_results)

    assert first_results[0].outcome is IngestionOutcome.IMPORTED
    assert second_results[0].outcome is IngestionOutcome.DUPLICATE
    assert second_results[0].document_id is None

    row_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM documents
        """
    ).fetchone()[0]

    assert row_count == 1


def test_ingest_documents_detects_renamed_duplicate(
    connection: sqlite3.Connection,
    tmp_path: Path,
) -> None:
    inbox_path = tmp_path / "inbox"
    inbox_path.mkdir()

    content = b"same synthetic statement"

    (inbox_path / "first.pdf").write_bytes(content)
    (inbox_path / "renamed.pdf").write_bytes(content)

    repository = DocumentRepository(connection)

    results = ingest_documents(inbox_path, repository)

    outcomes = [result.outcome for result in results]

    assert outcomes.count(IngestionOutcome.IMPORTED) == 1
    assert outcomes.count(IngestionOutcome.DUPLICATE) == 1

    row_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM documents
        """
    ).fetchone()[0]

    assert row_count == 1
