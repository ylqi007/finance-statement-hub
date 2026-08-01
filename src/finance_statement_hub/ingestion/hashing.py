import hashlib
from pathlib import Path

DEFAULT_CHUNK_SIZE = 1024 * 1024


def calculate_sha256(
    file_path: Path,
    *,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> str:
    """Calculate the SHA-256 digest of a file.

    The file is read in chunks so large statements do not need to be loaded
    entirely into memory.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if not file_path.exists():
        raise FileNotFoundError(f"file does not exist: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"path is not a file {file_path}")

    digest = hashlib.sha256()

    with file_path.open("rb") as source:
        while chunk := source.read(chunk_size):
            digest.update(chunk)

    return digest.hexdigest()
