"""Implementation of a recursive depth-first search algorithm.

This module provides a function that performs depth-first traversal
of a graph to find a path between two nodes.
"""


def depth_first_search(startnode, goalnode):
    """Search for a path from startnode to goalnode using depth-first search.

    Explores as far as possible along each branch before backtracking,
    using recursion to traverse the graph.

    Args:
        startnode: The node to start the search from
        goalnode: The target node to find

    Returns:
        bool: True if there is a path from startnode to goalnode, False otherwise
    """
    nodesvisited = set()

    def search_from(node):
        if node in nodesvisited:
            return False
        elif node is goalnode:
            return True
        else:
            nodesvisited.add(node)
            return any(search_from(nextnode) for nextnode in node.successors)

    return search_from(startnode)
