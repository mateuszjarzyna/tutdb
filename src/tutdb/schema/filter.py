from abc import ABC, abstractmethod
from typing import Any

from .column import Column
from ..schema.row import Value, Row


def equals(left: Column, right: Any) -> 'Condition':
    return EqualsCondition(left, right)


def less_than(left: Column, right: Any) -> 'Condition':
    return LessThan(left, right)


class Where:
    def __init__(self, condition: 'Condition'):
        self._condition: Condition = condition

    def match(self, row: Row) -> bool:
        return self._condition.match(row)


class Condition(ABC):
    def __init__(self, left_column: Column, right_value: Any):
        self._left_column = left_column
        self._right_value = right_value
        self._and: Condition | None = None
        self._or: Condition | None = None

    def and_condition(self, other: 'Condition') -> 'Condition':
        if self._or is not None:
            raise ValueError("OR condition already set")
        self._and = other
        return self

    def or_condition(self, other: 'Condition') -> 'Condition':
        if self._and is not None:
            raise ValueError("AND condition already set")
        self._or = other
        return self

    def match(self, row: Row) -> bool:
        left_value = row.get_value(self._left_column)
        match_self = self._match(left_value, self._right_value)
        if self._and is not None:
            return match_self and self._and.match(row)
        elif self._or is not None:
            return match_self or self._or.match(row)
        else:
            return match_self

    @abstractmethod
    def _match(self, left: Value, right: Any) -> bool:
        pass


class EqualsCondition(Condition):
    def __init__(self, left_column: Column, right_column: Column):
        super().__init__(left_column, right_column)

    def _match(self, left: Value, right: Any) -> bool:
        return left.get_value() == right


class LessThan(Condition):
    def __init__(self, left_column: Column, right_column: Column):
        super().__init__(left_column, right_column)

    def _match(self, left: Value, right: Any) -> bool:
        return left.as_int() < int(right)
