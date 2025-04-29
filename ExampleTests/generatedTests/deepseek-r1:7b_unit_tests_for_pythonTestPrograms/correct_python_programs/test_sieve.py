def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if not any(n % p == 0 for p in primes):
            primes.append(n)
    return primes

import unittest

class TestSieve(unittest.TestCase):
    def test_sieve(self):
        for sieve_implementation in [sieve]:
            primes = sieve_(50)  # Adjust N as needed
            self.assertEqual(primes, [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47])
            
if __name__ == '__main__':
    unittest.main()
```

To run the tests:
```bash
python your_script.py