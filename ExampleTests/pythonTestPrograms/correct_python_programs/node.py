"""Node class implementation for graph and tree data structures."""


class Node:
    """Represents a node in a graph or tree structure."""

    def __init__(
        self,
        value=None,
        children=None,
        parent=None,
        successors=None,
        predecessors=None,
    ):
        """Initialize a new Node instance.

        Args:
            value: The value stored in the node.
            children: List of child nodes.
            parent: Parent node.
            successors: List of successor nodes.
            predecessors: List of predecessor nodes.
        """
        self.value = value
        self.children = children if children is not None else []
        self.parent = parent
        self.successors = successors if successors is not None else []
        self.predecessors = predecessors if predecessors is not None else []

    def add_child(self, child):
        """Add a child node to this node.

        Args:
            child: The node to add as a child.
        """
        self.children.append(child)
        child.parent = self

    def add_successor(self, successor):
        """Add a successor node to this node.

        Args:
            successor: The node to add as a successor.
        """
        self.successors.append(successor)
        successor.predecessors.append(self)

    def __str__(self):
        """Return a string representation of the node.

        Returns:
            String representation of the node's value.
        """
        return str(self.value)
