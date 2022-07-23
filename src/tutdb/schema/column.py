from dataclasses import dataclass
from enum import Enum


class ColumnType(Enum):
    TEXT = 1
    INTEGER = 2


@dataclass
class ColumnSchema:
    index: int
    name: str
    type: ColumnType
