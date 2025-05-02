import string
import unittest

def to_base(num, b):
    result = ''
    alphabet = string.digits + string.ascii_uppercase
    while num > 0:
        i = num % b
        num = num // b
        result += alphabet[i]
    return result[::-1]

class TestToBase(unittest.TestCase):

    def test_to_base(self):
        self.assertEqual(to_base(255, 16), 'FF')
        self.assertEqual(to_base(-10, 2), '11110101') # Negative numbers are not supported
        self.assertEqual(to_base(0, 3), '')
        
if __name__ == '__main__':
    unittest.main()