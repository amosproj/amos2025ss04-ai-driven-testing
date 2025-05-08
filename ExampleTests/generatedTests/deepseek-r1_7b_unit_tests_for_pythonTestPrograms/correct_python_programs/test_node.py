class Node:
    def __init__(self, value=None, **kwargs):
        self.value = value
        if "predecessor" in kwargs:
            self.predecessor = kwargs["predecessor"]
        else:
            self.predecessor = []

    def get_predecessors(self):
        return self.predecessor.copy()
