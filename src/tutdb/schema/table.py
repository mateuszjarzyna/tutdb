from dataclasses import dataclass, field
from typing import List

from .column import ColumnSchema, ColumnType


@dataclass
class TableSchema:
    name: str
    columns: List[ColumnSchema] = field(default_factory=list)

    def add_column(self, column_name: str, column_type: ColumnType):
        column_index = len(self.columns)
        self.columns.append(ColumnSchema(index=column_index, name=column_name, type=column_type))

    def get_column_at_index(self, index: int):
        return self.columns[index]
