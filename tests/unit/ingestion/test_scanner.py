from pathlib import Path

import pytest

from finance_statement_hub.ingestion.hashing import calculate_sha256
from finance_statement_hub.ingestion.scanner import discover_documents


def test_discover_documents_finds_pdf_files_recursively(
    tmp_path: Path,
) -> None:
    nested_directory = tmp_path / "bank"
    nested_directory.mkdir()

    first_pdf = tmp_path / "credit-card.pdf"
    second_pdf = nested_directory / "checking.PDF"

    first_pdf.write_bytes(b"credit card statement")
    second_pdf.write_bytes(b"checking statement")

    documents = discover_documents(tmp_path)

    assert [document.file_name for document in documents] == [
        "checking.PDF",
        "credit-card.pdf",
    ]

    discovered_by_name = {document.file_name: document for document in documents}

    assert discovered_by_name["credit-card.pdf"].sha256 == (calculate_sha256(first_pdf))
    assert discovered_by_name["checking.PDF"].extension == ".pdf"


def test_discover_documents_ignores_unsupported_files(
    tmp_path: Path,
) -> None:
    pdf_file = tmp_path / "statement.pdf"
    text_file = tmp_path / "notes.txt"

    pdf_file.write_bytes(b"statement")
    text_file.write_text("private notes")

    documents = discover_documents(tmp_path)

    assert len(documents) == 1
    assert documents[0].file_name == "statement.pdf"


def test_discover_documents_returns_empty_list_for_empty_directory(
    tmp_path: Path,
) -> None:
    assert discover_documents(tmp_path) == []


def test_discover_documents_rejects_missing_directory(
    tmp_path: Path,
) -> None:
    missing_directory = tmp_path / "missing"

    with pytest.raises(
        FileNotFoundError,
        match="inbox directory does not exist",
    ):
        discover_documents(missing_directory)


def test_discover_documents_rejects_file_as_inbox(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "statement.pdf"
    file_path.write_bytes(b"statement")

    with pytest.raises(
        ValueError,
        match="inbox path is not a directory",
    ):
        discover_documents(file_path)
