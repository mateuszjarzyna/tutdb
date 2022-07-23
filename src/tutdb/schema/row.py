from dataclasses import dataclass
from typing import List, Any

from .column import ColumnsSchema, Column, ColumnType


@dataclass
class Value:
    column_index: int
    column_type: ColumnType
    bytes: bytes

    def __init__(self, column: Column, value: Any):
        self.column_index = column.index
        self.column_type = column.type
        self.bytes = value_to_bytes(column.type, value)

    def as_int(self):
        if self.column_type != ColumnType.INTEGER:
            raise ValueError("Column is not a number")
        return int.from_bytes(self.bytes, "big", signed=True)

    def as_string(self):
        if self.column_type != ColumnType.TEXT:
            raise ValueError("Column is not a string")
        return str(self.bytes, "utf-8")

    def get_value(self) -> Any:
        match self.column_type:
            case ColumnType.TEXT:
                return self.as_string()
            case ColumnType.INTEGER:
                return self.as_int()


def value_to_bytes(column_type: ColumnType, value: Any) -> bytes:
    match column_type:
        case ColumnType.TEXT:
            return bytes(str(value), "utf-8")
        case ColumnType.INTEGER:
            as_int = int(value)
            return as_int.to_bytes((as_int.bit_length() + 7) // 8, "big", signed=True)
    raise ValueError("Column type'" + str(column_type) + "' not supported")


class Row:
    def __init__(self, columns_schema: ColumnsSchema, values: dict[str, Any]):
        self._column_schema: ColumnsSchema = columns_schema
        self._values: List[Value] = sorted(create_values_list(columns_schema, values), key=lambda v: v.column_index)

    def get_value(self, column: Column) -> Value:
        return self._values[column.index]

    def get_as_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for column in self._column_schema.get_as_list():
            result[column.name] = self.get_value(column).get_value()
        return result


def create_values_list(schema: ColumnsSchema, values: dict[str, Any]) -> List[Value]:
    return [Value(get_column(schema, column_name), value) for column_name, value in values.items()]


def get_column(columns_schema: ColumnsSchema, column_name: str) -> Column:
    return columns_schema.get_column_by_name(column_name)
