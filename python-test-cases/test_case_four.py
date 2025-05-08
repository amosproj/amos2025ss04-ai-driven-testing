"""Module for finding Hamiltonian paths in undirected graphs.

This module provides a Graph class that can find all possible Hamiltonian paths
(paths that visit each node exactly once) from a given starting vertex in an
undirected graph represented as a collection of edges.
"""

from collections import defaultdict
from typing import Dict, List, Set


class Graph:
    """A class representing an undirected graph.

    This class implements functionality to find all Hamiltonian paths
    starting from a given vertex.
    """

    def __init__(self, edges):
        """Initialize a graph with a list of edges.

        Args:
            edges: A list of tuples where each tuple (u, v) represents
                  an undirected edge between vertices u and v
        """
        self.edges = edges
        self.graph: Dict[int, Set] = defaultdict(set)
        self.visited = defaultdict(lambda: False)

        self.make_graph(edges)

        self.visited_nodes = 0
        self.total_nodes = len(self.graph.keys())

    def make_graph(self, _edges) -> None:
        """Build the adjacency list representation of the graph.

        Adds the provided edges to the graph's adjacency list, ensuring
        each edge is represented in both directions (undirected graph).

        Args:
            _edges: A list of tuples where each tuple represents an edge
        """
        self.edges.extend(_edges)

        for u, v in self.edges:
            self.graph[u].add(v)
            self.graph[v].add(u)

    def visit(self, node):
        """Mark a node as visited.

        Args:
            node: The node to mark as visited
        """
        self.visited[node] = True
        self.visited_nodes += 1

    def un_visit(self, node):
        """Mark a node as unvisited (for backtracking).

        Args:
            node: The node to mark as unvisited
        """
        self.visited[node] = False
        self.visited_nodes -= 1

    def all_nodes_are_visited(self) -> bool:
        """Check if all nodes in the graph have been visited.

        Returns:
            bool: True if all nodes have been visited, False otherwise
        """
        return self.visited_nodes == self.total_nodes

    def get_hamiltonian_path(self, start) -> List[List[int]]:
        """Find all Hamiltonian paths starting from a given node.

        Uses a recursive backtracking approach to find all possible paths
        that visit each node in the graph exactly once.

        Args:
            start: The node to start the path from

        Returns:
            List[List[int]]: A list of all Hamiltonian paths, where each path
                            is represented as a list of nodes
        """
        self.visit(start)

        all_paths = []

        if self.all_nodes_are_visited():
            all_paths.append([start])

        for node in self.graph[start]:
            if self.visited[node]:
                continue
            paths = self.get_hamiltonian_path(node)
            for path in paths:
                if path:
                    path.append(start)
                    all_paths.append(path)

        self.un_visit(start)
        return all_paths


if __name__ == "__main__":
    edges = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4), (1, 3)]
    graph = Graph(edges)
    hamiltonian_path = graph.get_hamiltonian_path(start=1)

    for path in hamiltonian_path:
        print("->".join(map(str, reversed(path))))
