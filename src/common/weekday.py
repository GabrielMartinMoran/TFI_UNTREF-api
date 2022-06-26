from enum import Enum


class Weekday(Enum):
    # Uses the same criteria as datetime lib
    # https://docs.python.org/3/library/datetime.html#datetime.datetime.weekday
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    @staticmethod
    def next_after(weekday: 'Weekday') -> 'Weekday':
        """
        Returns the next weekday of the given weekday
        """
        next_weekday_value = weekday.value + 1 if weekday.value < Weekday.SUNDAY.value else Weekday.MONDAY.value
        return Weekday(next_weekday_value)

    @staticmethod
    def days_between(first: 'Weekday', second: 'Weekday') -> int:
        pointer = first
        days = 0
        while pointer.value != second.value:
            pointer = Weekday.next_after(pointer)
            days += 1
        return days
