import sys
from pathlib import Path
sys.path.insert(0, '/code/extracted')  # Add extracted dir to import path
from prompt import *  # Import functions from prompt.py

import unittest
from graph import Graph


class TestGraph(unittest.TestCase):
    def test_all_nodes_are_visited(self):
        # Create instance of Graph with list of edges
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4), (1, 3)]
        graph = Graph(edges)

        # Check if all nodes are visited
        self.assertTrue(graph.all_nodes_are_visited())

    def test_get_hamiltonian_path(self):
        # Create instance of Graph with list of edges
        edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4), (1, 3)]
        graph = Graph(edges)
        # Find all Hamiltonian paths starting from the given node
        all_paths = list()
        for node in graph.graph:
            if graph.visited[node]:
                continue
            paths = graph.get_hamiltonian_path(node)
            all_paths.extend(paths)
        # Check if all paths are found
        self.assertTrue(all_paths)
