import unittest
from string import digits, ascii_uppercase

def to_base(num, b):
    result = ''
    alphabet = digits + ascii_uppercase
    while num > 0:
        i = num % b
        num = num // b
        result = alphabet[i] + result
    return result

class TestToBase(unittest.TestCase):

    def test_to_base_10(self):
        self.assertEqual(to_base(10, 2), '1010')
        self.assertEqual(to_base(10, 3), '101')
        self.assertEqual(to_base(10, 4), '22')
        self.assertEqual(to_base(10, 5), '20')

    def test_to_base_16(self):
        self.assertEqual(to_base(10, 16), 'A')
        self.assertEqual(to_base(255, 16), 'FF')
        self.assertEqual(to_base(4095, 16), 'FFF')
        self.assertEqual(to_base(65535, 16), 'FFFF')

    def test_to_base_8(self):
        self.assertEqual(to_base(10, 8), '12')
        self.assertEqual(to_base(255, 8), '377')
        self.assertEqual(to_base(4095, 8), '7777')

    def test_to_base_single_digit(self):
        for i in range(10):
            self.assertEqual(to_base(i, 10), str(i))
        for i in range(26):
            self.assertEqual(to_base(i, 36), ascii_uppercase[i])

if __name__ == '__main__':
    unittest.main()