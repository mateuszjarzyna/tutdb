from dataclasses import dataclass
from typing import List
from enum import Enum


class ColumnType(Enum):
    TEXT = 1
    INTEGER = 2


@dataclass
class Column:
    index: int
    name: str
    type: ColumnType


class ColumnsSchema:
    def __init__(self):
        self._columns: List[Column] = []

    def add_column(self, column_name: str, column_type: ColumnType):
        column_index = len(self._columns)
        self._columns.append(Column(index=column_index, name=column_name, type=column_type))

    def get_column_at_index(self, index: int) -> Column:
        return self._columns[index]

    def get_column_by_name(self, name: str) -> Column:
        for column in self._columns:
            if column.name == name:
                return column
        raise ValueError("Column '" + name + "' not exist")

    def get_as_list(self) -> List[Column]:
        return self._columns
