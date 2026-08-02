import sqlite3
from pathlib import Path

from finance_statement_hub.database.document_repository import DocumentRepository
from finance_statement_hub.ingestion.models import DocumentIngestionResult, IngestionOutcome
from finance_statement_hub.ingestion.scanner import discover_documents


def ingest_documents(
    inbox_path: Path,
    repository: DocumentRepository,
) -> list[DocumentIngestionResult]:
    """Discover and register previouly unseen documents."""

    results: list[DocumentIngestionResult] = []

    for document in discover_documents(inbox_path):
        if repository.exists_by_sha256(document.sha256):
            results.append(
                DocumentIngestionResult(
                    document=document,
                    outcome=IngestionOutcome.DUPLICATE,
                )
            )
            continue

        try:
            document_id = repository.add(document)
        except sqlite3.IntegrityError:
            # The database UNIQUE constraint remains the final safeguard.
            results.append(
                DocumentIngestionResult(
                    document=document,
                    outcome=IngestionOutcome.DUPLICATE,
                )
            )
            continue

        results.append(
            DocumentIngestionResult(
                document=document,
                outcome=IngestionOutcome.IMPORTED,
                document_id=document_id,
            )
        )

    return results
