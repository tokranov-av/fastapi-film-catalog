import random
from unittest import TestCase


def add_two_numbers(number1: int, number2: int) -> int:
    return number1 + number2


class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self) -> None:
        number1 = random.randint(1, 100)  # noqa: S311
        number2 = random.randint(1, 100)  # noqa: S311
        expected = number1 + number2

        result = add_two_numbers(number1, number2)

        self.assertEqual(expected, result)
