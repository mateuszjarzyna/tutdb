import unittest

from src.tutdb.schema import TableSchema
from src.tutdb.schema.column import ColumnsSchema, ColumnType, Column
from src.tutdb.schema.row import Row
from src.tutdb.schema.filter import equals, Where, less_than


class FilterTest(unittest.TestCase):
    def test_equals_text_match(self):
        # given
        schema, name_column, _ = create_columns_schema()
        # and
        john = young_john(schema)
        # and
        condition = equals(name_column, "John")
        where = Where(condition)

        # when
        match = where.matches(john)

        # then
        self.assertTrue(match)

    def test_equals_text_not_match(self):
        # given
        schema, name_column, _ = create_columns_schema()
        # and
        john = young_john(schema)
        # and
        condition = equals(name_column, "Kate")
        where = Where(condition)

        # when
        match = where.matches(john)

        # then
        self.assertFalse(match)

    def test_equals_integer_match(self):
        # given
        schema, _, age_column = create_columns_schema()
        # and
        john = young_john(schema)
        # and
        condition = equals(age_column, 23)
        where = Where(condition)

        # when
        match = where.matches(john)

        # then
        self.assertTrue(match)

    def test_equals_integer_not_match(self):
        # given
        schema, _, age_column = create_columns_schema()
        # and
        john = young_john(schema)
        # and
        condition = equals(age_column, 87)
        where = Where(condition)

        # when
        match = where.matches(john)

        # then
        self.assertFalse(match)

    def test_less_than_match(self):
        # given
        schema, _, age_column = create_columns_schema()
        # and
        john = young_john(schema)
        # and
        condition = less_than(age_column, 100)
        where = Where(condition)

        # when
        match = where.matches(john)

        # then
        self.assertTrue(match)

    def test_less_than_not_match(self):
        # given
        schema, _, age_column = create_columns_schema()
        # and
        john = young_john(schema)
        # and
        condition = less_than(age_column, 5)
        where = Where(condition)

        # when
        match = where.matches(john)

        # then
        self.assertFalse(match)

    def test_and_match(self):
        # given
        schema, name_column, age_column = create_columns_schema()
        # and
        john = young_john(schema)
        # and
        condition = equals(name_column, "John").and_condition(less_than(age_column, 50))
        where = Where(condition)

        # when
        match = where.matches(john)

        # then
        self.assertTrue(match)

    def test_and_not_match_age(self):
        # given
        schema, name_column, age_column = create_columns_schema()
        # and
        john = young_john(schema)
        # and
        condition = equals(name_column, "John").and_condition(less_than(age_column, 5))
        where = Where(condition)

        # when
        match = where.matches(john)

        # then
        self.assertFalse(match)

    def test_and_match_name(self):
        # given
        schema, name_column, age_column = create_columns_schema()
        # and
        john = young_john(schema)
        kate = old_kate(schema)
        # and
        condition = equals(name_column, "Kate").and_condition(less_than(age_column, 50))
        where = Where(condition)

        # when
        match_john = where.matches(john)
        # and
        match_kate = where.matches(kate)

        # then
        self.assertFalse(match_john)
        # and
        self.assertFalse(match_kate)

    def test_or_match_one_condition_for_each(self):
        # given
        schema, name_column, age_column = create_columns_schema()
        # and
        john = young_john(schema)
        kate = old_kate(schema)
        # and
        condition = equals(name_column, "Kate").or_condition(less_than(age_column, 40))
        where = Where(condition)

        # when
        match_john = where.matches(john)
        # and
        match_kate = where.matches(kate)

        # then
        self.assertTrue(match_john)
        # and
        self.assertTrue(match_kate)

    def test_or_match_both(self):
        # given
        schema, name_column, age_column = create_columns_schema()
        # and
        john = young_john(schema)
        kate = old_kate(schema)
        # and
        condition = equals(name_column, "Kate").or_condition(less_than(age_column, 100))
        where = Where(condition)

        # when
        match_john = where.matches(john)
        # and
        match_kate = where.matches(kate)

        # then
        self.assertTrue(match_john)
        # and
        self.assertTrue(match_kate)

    def test_or_match_name(self):
        # given
        schema, name_column, age_column = create_columns_schema()
        # and
        john = young_john(schema)
        kate = old_kate(schema)
        # and
        condition = equals(name_column, "Kate").or_condition(less_than(age_column, 5))
        where = Where(condition)

        # when
        match_john = where.matches(john)
        # and
        match_kate = where.matches(kate)

        # then
        self.assertFalse(match_john)
        # and
        self.assertTrue(match_kate)

    def test_empty_where(self):
        # given
        schema, name_column, age_column = create_columns_schema()
        # and
        john = young_john(schema)
        kate = old_kate(schema)
        # and
        where = Where()

        # when
        match_john = where.matches(john)
        # and
        match_kate = where.matches(kate)

        # then
        self.assertTrue(match_john)
        # and
        self.assertTrue(match_kate)


def create_columns_schema() -> (ColumnsSchema, Column, Column):
    table = TableSchema("employee")
    table.add_column("name", ColumnType.TEXT)
    table.add_column("age", ColumnType.INTEGER)

    columns = table.columns
    return columns, columns.get_column_by_name("name"), columns.get_column_by_name("age")


def young_john(schema: ColumnsSchema) -> Row:
    values = {
        "name": "John",
        "age": 23
    }
    return Row(schema, values)


def old_kate(schema: ColumnsSchema) -> Row:
    values = {
        "name": "Kate",
        "age": 87
    }
    return Row(schema, values)


if __name__ == '__main__':
    unittest.main()
