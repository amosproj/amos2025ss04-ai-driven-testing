import unittest


def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if all(n % p > 0 for p in primes):
            primes.append(n)
    return primes


class TestSieve(unittest.TestCase):
    def test_sieve_empty_range(self):
        self.assertEqual(sieve(1), [])
        self.assertEqual(sieve(1), [])

    def test_sieve_small_range(self):
        self.assertEqual(sieve(10), [2, 3, 5, 7])
        self.assertEqual(sieve(10), [2, 3, 5, 7])
        self.assertEqual(sieve(5), [2, 3, 5])

    def test_sieve_large_range(self):
        self.assertEqual(sieve(20), [2, 3, 5, 7, 11, 13, 17, 19])

    def test_sieve_single_prime(self):
        self.assertEqual(sieve(2), [2])

    def test_sieve_no_primes(self):
        self.assertEqual(sieve(4), [2, 3])
        self.assertEqual(sieve(4), [2, 3])


if __name__ == "__main__":
    unittest.main()
