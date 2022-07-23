from typing import List

from .column import Column, ColumnType, ColumnsSchema


class TableSchema:
    def __init__(self, name):
        self.name = name
        self.columns = ColumnsSchema()

    def add_column(self, column_name: str, column_type: ColumnType):
        self.columns.add_column(column_name, column_type)

    def get_column_at_index(self, index: int) -> Column:
        return self.columns.get_column_at_index(index)

    def get_columns(self) -> List[Column]:
        return self.columns.get_as_list()
