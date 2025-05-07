import unittest


def bitcount(n):
    """Count number of 1's in binary representation."""
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


class TestBitCount(unittest.TestCase):

    
# Testing integer values for correctness.
    def test_bit_count_of_positive_integer(self):
        self.assertEqual(bitcount(5), 2)   # Binary: 101 -> Count = 2

    def test_bit_count_of_zero(self):
        self.assertEqual(bitcount(0), 0)

    def test_bit_count_negative_number(self):
        with self.assertRaises(TypeError):  # Expecting a TypeError as per the original function behavior.
            bitcount(-5)


if __name__ == '__main__':
    unittest.main()