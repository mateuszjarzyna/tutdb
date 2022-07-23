import unittest

from src.tutdb.in_memory_databse.in_memory_table import InMemoryTable
from src.tutdb.schema import TableSchema
from src.tutdb.schema.column import ColumnType


class InMemoryTableTest(unittest.TestCase):
    def test_insert_row(self):
        # given
        schema = create_columns_schema()
        # and
        table = InMemoryTable(schema)
        # and
        values = {
            "name": "John",
            "age": 23
        }

        # when
        table.insert_row(values)
        # and
        table.insert_row(values)

        # then
        self.assertEqual(table.count(), 2)


def create_columns_schema() -> TableSchema:
    table = TableSchema("employee")
    table.add_column("name", ColumnType.TEXT)
    table.add_column("age", ColumnType.INTEGER)
    return table


if __name__ == '__main__':
    unittest.main()
