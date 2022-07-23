import unittest

from src.tutdb.schema import TableSchema
from src.tutdb.schema.column import ColumnsSchema, ColumnType, Column
from src.tutdb.schema.row import Row


class RowTest(unittest.TestCase):
    def test_add_values(self):
        # given
        schema, name_column, age_column = create_columns_schema()
        # and
        values = {
            "name": "John",
            "age": 23
        }

        # when
        row = Row(schema, values)

        # then
        self.assertEqual(row.get_value(name_column).as_string(), "John")
        # and
        self.assertEqual(row.get_value(age_column).as_int(), 23)

    def test_non_ascii_chars_and_negative_number(self):
        # given
        schema, name_column, age_column = create_columns_schema()
        # and
        values = {
            "name": "żółć",
            "age": -12
        }

        # when
        row = Row(schema, values)

        # then
        self.assertEqual(row.get_value(name_column).as_string(), "żółć")
        # and
        self.assertEqual(row.get_value(age_column).as_int(), -12)

    def test_get_value_as_any_object(self):
        # given
        schema, name_column, age_column = create_columns_schema()
        # and
        values = {
            "name": "John",
            "age": 23
        }

        # when
        row = Row(schema, values)

        # then
        self.assertEqual(row.get_value(name_column).get_value(), "John")
        # and
        self.assertEqual(row.get_value(age_column).get_value(), 23)

    def test_get_values_as_dictionary(self):
        # given
        schema, name_column, age_column = create_columns_schema()
        # and
        values = {
            "name": "John",
            "age": 23
        }

        # when
        row = Row(schema, values)

        # then
        expected_values = {
            "age": 23,
            "name": "John"
        }
        self.assertEqual(row.get_as_dict(), expected_values)


def create_columns_schema() -> (ColumnsSchema, Column, Column):
    table = TableSchema("employee")
    table.add_column("name", ColumnType.TEXT)
    table.add_column("age", ColumnType.INTEGER)

    columns = table.columns
    return columns, columns.get_column_by_name("name"), columns.get_column_by_name("age")


if __name__ == '__main__':
    unittest.main()
