# Original sieve function
def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if all(n % p > 0 for p in primes):
            primes.append(n)
    return primes

# Testclass implementation
import unittest

from correct_python_programs.sievefromcorrect_python_programsfromcorrect_python_programs import \
    sieve
from unittestfromcorrect_python_programsfromcorrect_python_programs import \
    TestCase


class SieveTestCase(unittest.TestCase)(TestCase):
    def test_sieve(self):
        # Test sieve function with different max values
        self.assertEqual(sieve(2), [2])
        self.assertEqual(sieve(3), [2, 3])
        self.assertEqual(sieve(4), [2, 3])
        self.assertEqual(sieve(5), [2, 3, 5])
        self.assertEqual(sieve(6), [2, 3, 5])

if __name__ == '__main__':
    unittest.main()
```

```python
"""
import unittest
from correct_python_programs.sieve from correct_python_programs from correct_python_programs import sieve

class SieveTestCase(unittest.TestCase)(TestCase):
    def test_sieve(self):
        # Test sieve function with different max values
        self.assertEqual(Sieve(2), [2])
        self.assertEqual(Sieve(3), [2, 3])
        self.assertEqual(Sieve(4), [2, 3])
        self.assertEqual(Sieve(5), [2, 3, 5])
        self.assertEqual(Sieve(6), [2, 3, 5])

if __name__ == '__main__':
    unittest.main()
"""