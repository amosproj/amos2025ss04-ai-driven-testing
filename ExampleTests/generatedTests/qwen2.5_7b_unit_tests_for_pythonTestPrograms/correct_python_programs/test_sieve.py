def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if not any(n % p == 0 for p in primes):
            primes.append(n)
    return primes


import unittest

class TestSieveFunction(unittest.TestCase):

    def test_sieve(self):
        self.assertEqual(sieve(10), [2, 3, 5, 7])
        self.assertEqual(sieve(20), [2, 3, 5, 7, 11, 13, 17, 19])
        self.assertEqual(sieve(1), [])
        self.assertEqual(sieve(2), [2])


if __name__ == '__main__':
    unittest.main()