from collections.abc import Iterable
from pathlib import Path

from finance_statement_hub.ingestion.hashing import calculate_sha256
from finance_statement_hub.ingestion.models import DocumentCandidate

SUPPORTED_EXTENSIONS = frozenset({".pdf"})


def discover_documents(
    inbox_path: Path,
    *,
    supported_extensions: Iterable[str] = SUPPORTED_EXTENSIONS,
) -> list[DocumentCandidate]:
    """Discover supported documents in an inbox directory."""

    if not inbox_path.exists():
        raise FileNotFoundError(f"inbox directory does not exist: {inbox_path}")

    if not inbox_path.is_dir():
        raise ValueError(f"inbox path is not a directory: {inbox_path}")

    normalized_extensions = {
        extension.lower() if extension.startswith(".") else f".{extension.lower()}"
        for extension in supported_extensions
    }

    document_paths = sorted(
        (
            path
            for path in inbox_path.rglob("*")
            if path.is_file() and path.suffix.lower() in normalized_extensions
        ),
        key=lambda path: str(path.relative_to(inbox_path)).lower(),
    )

    return [
        DocumentCandidate(
            path=path,
            file_name=path.name,
            extension=path.suffix.lower(),
            size_bytes=path.stat().st_size,
            sha256=calculate_sha256(path),
        )
        for path in document_paths
    ]
