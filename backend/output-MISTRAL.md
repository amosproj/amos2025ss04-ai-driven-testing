 To write unit tests for the `add_numbers` function in Python, we can use a testing framework like pytest. Here is an example of how the test file might look:

```python
import pytest

def test_add_numbers():
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(0.5, 0.5) == 1.0
    assert add_numbers("2", "3") is None
    # Add more edge cases as needed

def test_invalid_input():
    with pytest.raises(TypeError):
        add_numbers(2, "3")
```

In this example, we have two test functions: `test_add_numbers` and `test_invalid_input`. The first function tests the correct behavior of the `add_numbers` function with various inputs. The second function checks if the function raises a TypeError when invalid input types are provided (e.g., strings instead of numbers).

You can run these tests using the command line like this:

```bash
pytest test_add_numbers.py
```

The output should show that the tests pass if the implementation of `add_numbers` function is correct. If not, you will see error messages indicating which tests failed.