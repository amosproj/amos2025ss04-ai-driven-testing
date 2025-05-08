import string
import unittest


def to_base(num, b):
    result = ""
    alphabet = string.digits + string.ascii_uppercase
    while num > 0:
        i = num % b
        num = num // b
        result = alphabet[i] + result
    return result


class TestToBase(unittest.TestCase):
    def test_to_base_valid(self):
        self.assertEqual(to_base(10, 2), "1010")
        self.assertEqual(to_base(10, 8), "12")
        self.assertEqual(to_base(10, 16), "A")
        self.assertEqual(to_base(10, 10), "10")
        self.assertEqual(to_base(10, 12), "A")
        self.assertEqual(to_base(10, 3), "101")

    def test_to_base_zero(self):
        self.assertEqual(to_base(0, 2), "")
        self.assertEqual(to_base(0, 8), "")
        self.assertEqual(to_base(0, 16), "")
        self.assertEqual(to_base(0, 10), "")
        self.assertEqual(to_base(0, 12), "")
        self.assertEqual(to_base(0, 3), "")

    def test_to_base_large_number(self):
        self.assertEqual(to_base(255, 16), "FF")
        self.assertEqual(to_base(65535, 16), "FF")


if __name__ == "__main__":
    unittest.main()
