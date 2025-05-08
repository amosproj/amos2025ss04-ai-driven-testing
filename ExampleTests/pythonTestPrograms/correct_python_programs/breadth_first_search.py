"""Implementation of the breadth-first search algorithm.

This module provides a function that performs breadth-first traversal
of a graph represented as an adjacency list.
"""

from collections import deque


def breadth_first_search(startnode, goalnode):
    """Search for a path from startnode to goalnode using breadth-first search.

    Explores all nodes at the present depth before moving to nodes at the next
    depth level, guaranteeing the shortest path in terms of number of edges.

    Args:
        startnode: The node to start the search from
        goalnode: The target node to find

    Returns:
        bool: True if there is a path from startnode to goalnode, False otherwise
    """
    queue = deque()
    queue.append(startnode)

    nodesseen = set()
    nodesseen.add(startnode)

    while queue:
        node = queue.popleft()

        if node is goalnode:
            return True
        else:
            queue.extend(
                node for node in node.successors if node not in nodesseen
            )
            nodesseen.update(node.successors)

    return False
