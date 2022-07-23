from typing import List, Any

from ..schema.row import Row
from ..schema.table import TableSchema


class InMemoryTable:
    def __init__(self, schema: TableSchema):
        self.schema: TableSchema = schema
        self._rows: List[Row] = []

    def insert_row(self, values: dict[str, Any]):
        new_row = Row(self.schema.columns, values)
        self._rows.append(new_row)

    def count(self) -> int:
        return len(self._rows)
    
