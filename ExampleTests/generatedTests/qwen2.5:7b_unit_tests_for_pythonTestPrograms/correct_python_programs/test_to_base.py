import string
from unittest import TestCase, main

def to_base(num, b):
    result = ''
    alphabet = string.digits + string.ascii_uppercase
    while num > 0:
        i = num % b
        num = num // b
        result = alphabet[i] + result
    return result

class TestToBaseFunction(TestCase):

    def test_to_base_10(self):
        self.assertEqual(to_base(10, 10), 'A')

    def test_to_base_9(self):
        self.assertEqual(to_base(9, 16), '9')

    def test_to_base_255(self):
        self.assertEqual(to_base(255, 16), 'FF')

    def test_to_base_30(self):
        self.assertEqual(to_base(30, 7), '54')

if __name__ == '__main__':
    main()