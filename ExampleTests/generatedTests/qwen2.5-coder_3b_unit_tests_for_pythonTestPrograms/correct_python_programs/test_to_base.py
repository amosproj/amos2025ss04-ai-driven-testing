import string
from unittest import TestCase


def to_base(num, b):
    result = ""
    alphabet = string.digits + string.ascii_uppercase
    while num > 0:
        i = num % b
        num = num // b
        result = alphabet[i] + result
    return result


class TestToBase(TestCase):
    def test_to_base(self):
        self.assertEqual(to_base(1, 2), "1")
        self.assertEqual(to_base(5, 3), "12")
        self.assertEqual(to_base(10, 4), "22")
        self.assertEqual(to_base(255, 8), "377")
        self.assertEqual(to_base(16, 2), "10000")


if __name__ == "__main__":
    unittest.main()
