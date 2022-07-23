import unittest
from typing import List

from src.tutdb.schema.row import Row
from src.tutdb.in_memory_databse.in_memory_table import InMemoryTable
from src.tutdb.schema import TableSchema
from src.tutdb.schema.column import ColumnType, Column
from src.tutdb.schema.filter import equals, Where, less_than


class InMemoryTableTest(unittest.TestCase):
    def test_insert_row(self):
        # given
        schema = create_table_schema()
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

    def test_find_all_with_empty_where(self):
        # given
        table, name_column, age_column = create_table_with_example_data()
        # and

        # when
        found = table.find()

        # then
        self.assertEqual(len(found), 2)
        # and
        self.assertTrue(has_row_with_name(found, "John"))
        self.assertTrue(has_row_with_name(found, "Kate"))

    def test_find_by_name(self):
        # given
        table, name_column, age_column = create_table_with_example_data()
        # and
        condition = equals(name_column, "John")
        where = Where(condition)

        # when
        found = table.find(where)

        # then
        self.assertEqual(len(found), 1)
        # and
        self.assertTrue(has_row_with_name(found, "John"))
        self.assertFalse(has_row_with_name(found, "Kate"))

    def test_find_by_name_or(self):
        # given
        table, name_column, age_column = create_table_with_example_data()
        # and
        condition = equals(name_column, "John").or_condition(equals(name_column, "Kate"))
        where = Where(condition)

        # when
        found = table.find(where)

        # then
        self.assertEqual(len(found), 2)
        # and
        self.assertTrue(has_row_with_name(found, "John"))
        self.assertTrue(has_row_with_name(found, "Kate"))

    def test_find_by_name_or_age(self):
        # given
        table, name_column, age_column = create_table_with_example_data()
        # and
        condition = equals(name_column, "John").or_condition(less_than(age_column, 100))
        where = Where(condition)

        # when
        found = table.find(where)

        # then
        self.assertEqual(len(found), 2)
        # and
        self.assertTrue(has_row_with_name(found, "John"))
        self.assertTrue(has_row_with_name(found, "Kate"))


def create_table_schema() -> TableSchema:
    table = TableSchema("employee")
    table.add_column("name", ColumnType.TEXT)
    table.add_column("age", ColumnType.INTEGER)
    return table


def create_table() -> InMemoryTable:
    schema = create_table_schema()
    return InMemoryTable(schema)


def create_table_with_example_data() -> (InMemoryTable, Column, Column):
    table = create_table()
    table.insert_row({"name": "John", "age": 23})
    table.insert_row({"name": "Kate", "age": 87})
    return table, get_column_from_schema(table, "name"), get_column_from_schema(table, "age")


def get_column_from_schema(table: InMemoryTable, column_name: str):
    return table.schema.columns.get_column_by_name(column_name)


def get_value_from_name_column(row: Row) -> str:
    return str(row.get_as_dict()['name'])


def has_row_with_name(found: List[Row], name: str) -> bool:
    return any(get_value_from_name_column(row) == name for row in found)


if __name__ == '__main__':
    unittest.main()
