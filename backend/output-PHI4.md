```markdown
# Unit Tests for `add_numbers` Function

Below are the unit tests to validate different scenarios of using the function `add_numbers`.

### Test Cases:

#### Case 1: Adding positive integers.
- Input: `(2, 3)`
- Expected Output: `5`

```python
def test_add_positive_integers():
    assert add_numbers(2, 3) == 5

test_add_positive_integers()
```

#### Case 2: Adding a negative integer and a positive integer (resulting in zero).
- Input: `(-1, 1)`
- Expected Output: `0`

```python
def test_add_negative_and_positive_integer():
    assert add_numbers(-1, 1) == 0

test_add_negative_and_positive_integer()
```

#### Case 3: Adding two positive floats.
- Input: `(0.5, 0.5)`
- Expected Output: `1.0`

```python
def test_add_two_floats():
    assert add_numbers(0.5, 0.5) == 1.0

test_add_two_floats()
```

#### Case 4: Adding a positive integer and zero.
- Input: `(3, 0)`
- Expected Output: `3` (should be included for completeness)

```python
def test_add_positive_integer_and_zero():
    assert add_numbers(3, 0) == 3

test_add_positive_integer_and_zero()
```

#### Case 5: Adding a negative integer and zero.
- Input: `( -2 , 0 )`
- Expected Output: `-2` (should be included for completeness)

```python
def test_add_negative_integer_and_zero():
    assert add_numbers(-2, 0) == -2

test_add_negative_integer_and_zero()
```

#### Case 6: Adding two negative integers.
- Input: `( -1 , -1 )`
- Expected Output: `-2` (should be included for completeness)

```python
def test_add_two_negative_integers():
    assert add_numbers(-1, -1) == -2

test_add_two_negative_integers()
```

### Notes:
Make sure to run these tests in an appropriate environment where you can execute Python code and see the results. The assertions will throw errors if any of them fail.
```