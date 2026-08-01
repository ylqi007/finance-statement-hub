import hashlib
from pathlib import Path

import pytest

from finance_statement_hub.ingestion.hashing import calculate_sha256


def test_calculate_sha256_returns_expected_digest(tmp_path: Path) -> None:

    print(f"\ntmp_path: {tmp_path}")

    file_path = tmp_path / "statement.pdf"
    print(f"file_path: {file_path}")

    content = b"synthetic financial statement"
    file_path.write_bytes(content)

    expected = hashlib.sha256(content).hexdigest()
    actual = calculate_sha256(file_path)

    print(f"expected: {expected}")
    print(f"actual:   {actual}")

    assert calculate_sha256(file_path) == expected


def test_calculate_sha256_supports_small_chunks(tmp_path: Path) -> None:
    file_path = tmp_path / "statement.pdf"
    content = b"abcdefghijklmnopqrstuvwxyz"
    file_path.write_bytes(content)

    expected = hashlib.sha256(content).hexdigest()

    assert calculate_sha256(file_path, chunk_size=3) == expected


def test_calculate_sha256_rejects_missing_file(tmp_path: Path) -> None:
    file_path = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError, match="file does not exist"):
        calculate_sha256(file_path)


def test_calculate_sha256_rejects_invalid_chunk_size(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "statement.pdf"
    file_path.write_bytes(b"content")

    with pytest.raises(
        ValueError,
        match="chunk_size must be greater than zero",
    ):
        calculate_sha256(file_path, chunk_size=0)
