import unittest

class TestSieve(unittest.TestCase):
    def test_sieve(self):
        self.assertEqual(sieve(10), [2, 3, 5, 7])
        self.assertEqual(sieve(1), [])
        self.assertEqual(sieve(29), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

if __name__ == '__main__':
    unittest.main()