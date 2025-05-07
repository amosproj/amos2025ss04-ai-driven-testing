import unittest


def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if all(n % p > 0 for p in primes):
            primes.append(n)
    return primes


class TestSieve(unittest.TestCase):
    def test_sieve_with_max_10(self):
        result = sieve(10)
        expected = [2, 3, 5, 7]
        self.assertEqual(result, expected)

    def test_sieve_with_max_20(self):
        result = sieve(20)
        expected = [2, 3, 5, 7, 11, 13, 17, 19]
        self.assertEqual(result, expected)

    def test_sieve_with_max_1(self):
        result = sieve(1)
        expected = []
        self.assertEqual(result, expected)

    def test_sieve_with_max_2(self):
        result = sieve(2)
        expected = [2]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
