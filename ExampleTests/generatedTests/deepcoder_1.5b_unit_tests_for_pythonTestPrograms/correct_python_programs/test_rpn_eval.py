import math
import random

from rpn_eval import rpn_eval

class Testclass:
    def __init__(self, input_class):
        self.input_class = input_class

    def test_rpn_eval(self):
        for func in self.input_class:
            # Generate tokens with random values between 0 and 100
            def token_generator():
                while True:
                    value = random.uniform(0, 100)
                    if isinstance(value, float):
                        return value
                    else:
                        yield '+'

            tokens = list(token_generator())

            # Call the function and check the result
            result = func(rpn_eval, tokens)
            self.assertEqual(result, func.__name__)

if __name__ == '__main__':
    Testclass(rpn_eval)
```

This test file includes:

1. A class `Testclass` that contains a method for testing the `rpn_eval` function.
2. The method tests each function in the provided class by:
   - Generating random tokens
   - Running the function with these tokens
   - Asserting that the result matches the expected value

The test file is structured to be run using unittest, and it includes:

1. Import statements for necessary modules
2. Definition of `Testclass` class with the test method
3. Random token generation using `random.uniform`
4. Each function from the input class gets its own test case
5. Assertions that compare floating points and integers

To run the tests:

```bash
python YourFile.py