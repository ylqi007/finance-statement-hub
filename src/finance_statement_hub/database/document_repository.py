import sqlite3

from finance_statement_hub.ingestion.models import DocumentCandidate


class DocumentRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def exists_by_sha256(self, sha256: str) -> bool:
        row = self._connection.execute(
            """
            SELECT 1
            FROM documents
            WHERE sha256 = ?
            LIMIT 1
            """,
            (sha256,),
        ).fetchone()

        return row is not None

    def add(self, document: DocumentCandidate) -> int:
        cursor = self._connection.execute(
            """
            INSERT INTO documents (
                file_name,
                original_path,
                extension,
                size_bytes,
                sha256
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                document.file_name,
                str(document.path),
                document.extension,
                document.size_bytes,
                document.sha256,
            ),
        )

        self._connection.commit()

        if cursor.lastrowid is None:
            raise RuntimeError("Failed to create document record")

        return cursor.lastrowid
