import unittest

from src.tutdb.schema.column import ColumnType
from src.tutdb.schema.table import TableSchema


def create_test_table():
    return TableSchema(name="employee")


class SchemaTest(unittest.TestCase):
    def test_create_table(self):
        # given
        table = TableSchema(name="employee")

        # expect
        self.assertEqual(table.name, "employee")
        self.assertEqual(len(table.get_columns()), 0)

    def test_add_columns(self):
        # given
        table = create_test_table()

        # when
        table.add_column("name", ColumnType.TEXT)
        table.add_column("age", ColumnType.INTEGER)

        # then
        self.assertEqual(len(table.get_columns()), 2)
        # and
        name_column = table.get_column_at_index(0)
        self.assertEqual(name_column.name, "name")
        self.assertEqual(name_column.type, ColumnType.TEXT)
        # and
        age_column = table.get_column_at_index(1)
        self.assertEqual(age_column.name, "age")
        self.assertEqual(age_column.type, ColumnType.INTEGER)


if __name__ == '__main__':
    unittest.main()
