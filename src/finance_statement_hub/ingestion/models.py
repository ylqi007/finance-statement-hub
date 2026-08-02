from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


# frozen=True 表示对象创建后不能被修改，可以降低 ingestion pipeline 中数据被意外改变的风险。
# slot=True 可以减少对象占用的内存，也阻止随意添加未定义的属性。
@dataclass(frozen=True, slots=True)
class DocumentCandidate:
    """A source document discovered before it is imported."""

    path: Path
    file_name: str
    extension: str
    size_bytes: int
    sha256: str


class IngestionOutcome(StrEnum):
    IMPORTED = "Imported"
    DUPLICATE = "Duplicate"


@dataclass(frozen=True, slots=True)
class DocumentIngestionResult:
    document: DocumentCandidate
    outcome: IngestionOutcome
    document_id: int | None = None
