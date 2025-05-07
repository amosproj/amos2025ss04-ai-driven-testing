from heapq import *
import unittest


class TestShortestPathLength(unittest.TestCase):
    def setUp(self):
        self.length_by_edge = {
            ("A", "B"): 5,
            ("B", "C"): 2,
            ("C", "D"): 4,
            ("A", "C"): 10,
        }
        self.startnode = "A"
        self.goalnode = "D"

    def test_shortest_path_length(self):
        # Test case 1: Simple path
        expected_distance = 6
        self.assertEqual(
            shortest_path_length(
                self.length_by_edge, self.startnode, self.goalnode
            ),
            expected_distance,
        )

        # Test case 2: Path through multiple nodes
        expected_distance = 7
        self.assertEqual(
            shortest_path_length(self.length_by_edge, "A", "C"),
            expected_distance,
        )

        # Test case 3: Goal node is not reachable
        self.assertEqual(
            shortest_path_length(self.length_by_edge, "A", "E"), float("inf")
        )

        # Test case 4: Single edge path
        self.assertEqual(shortest_path_length({("A", "B"): 3}, "A", "B"), 3)

        # Test case 5: Edge case with only one node
        self.assertEqual(shortest_path_length({}, "A", "A"), 0)


if __name__ == "__main__":
    unittest.main()
