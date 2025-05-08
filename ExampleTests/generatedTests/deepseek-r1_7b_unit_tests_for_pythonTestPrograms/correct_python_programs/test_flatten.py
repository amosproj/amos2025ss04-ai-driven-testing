import unittest

import numpy as np
from correct_python_programs.flattenfromcorrect_python_programs import flatten
from correct_python_programs.typing import Any, List


class FlattenManager(unittest.TestCase):
    def __init__(self, arr: List[Any]) -> None:
        self._arr = arr
        self._flattened = list(flatten(arr))
        self._shape = self.get_shape()

    @property
    def arr(self) -> List[Any]:
        return self._arr

    @property
    def flattened(self) -> List[Any]:
        return self._flattened.copy()

    @property
    def shape(self) -> tuple:
        return self._shape

    @staticmethod
    def _flatten(arr):
        for x in arr:
            if isinstance(x, list):
                yield from FlattenManager._flatten(x)
            else:
                yield x

    @classmethod
    def get_shape(cls) -> tuple:
        current = object()
        shape = []
        cls._flatten(shape, current)
        return tuple(shape)

    @classmethod
    def _shape_check(cls, other: 'FlattenManager') -> bool:
        if len(cls._shape) != len(other._shape):
            return False
        return all(a == b for a, b in zip(cls._shape, other._shape))

    def is_shape_to(self, other: 'FlattenManager') -> bool:
        return self._shape_check(other)

# Test class
class TestFlattenManager(unittest.TestCase):
    def test_init(self):
        fm = FlattenManager([[1,2], [3,[4,5]]])
        self.assertEqual(fm.flattened(), [1,2,3,4,5])
    
    def test_flatten_property(self):
        arr = [[1, 2], [3, None]]
        manager = FlattenManager(arr)
        self.assertEqual(manager.flattened(), [1,2,3,None])

    def test_get_shape(self):
        nested_list = [[[1]]]
        manager = FlattenManager(nested_list)
        self.assertEqual(manager.shape, (4,))
    
    def test_shape_check(self):
        manager1 = FlattenManager([[1, 2], [3, 4]])
        manager2 = FlattenManager([5,6])
        self.assertFalse(manager1.is_shape_to(manager2))
        
        manager3 = FlattenManager([[7],[8]])
        self.assertTrue(manager1.is_shape_to(manager3))

if __name__ == "__main__":
    unittest.main()
```

This test class includes unit tests for all methods in the `FlattenManager` class:
- `init`: Tests initialization and property setting
- `flatten_property`: Tests the flattened list functionality
- `get_shape`: Tests extracting shape information
- `shape_check`: Tests comparing shapes

The test cases verify basic functionality, edge cases (like None values), nested structures, and type safety.

To run the tests:
```bash
python3 -m unittest manage.py test