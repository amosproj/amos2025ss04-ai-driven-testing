import unittest

class TestTopologicalOrder:
    def test_topological_order_valid_order(self):
        # Create nodes A -> B -> C and A -> D
        node_A = Node(incoming_nodes=[])
        node_B = Node(incoming_nodes=[node_A])
        node_C = Node(incoming_nodes=[node_B])
        node_D = Node(incoming_nodes=[node_A])
        
        ordered_nodes = topological_ordering([node_A, node_B, node_C, node_D])
        
        self.assertEqual(ordered_nodes, [node_A, node_B, node_C, node_D])

    def test_topological_order_nodes_with_no_dependencies(self):
        # Create nodes with no dependencies
        node_X = Node(incoming_nodes=[])
        node_Y = Node(incoming_nodes=[])
        
        ordered_nodes = topological_ordering([node_X, node_Y])
        
        # Either X or Y should come first since they have same priority
        expected_order = [node_X, node_Y]  # Possible outcomes could be different orders
        
        self.assertIn(node_X, ordered_nodes)
        self.assertIn(node_Y, ordered_nodes)

    def test_topological_order_cyclic_graph(self):
        # Create a cyclic graph A->B->C->A and D
        node_A = Node(incoming_nodes=[node_C])
        node_B = Node(incoming_nodes=[node_A])
        node_C = Node(incoming_nodes=[node_B])
        
        ordered_nodes = topological_ordering([node_D, node_A, node_B, node_C])
        
        # D should be first since it has no dependencies
        self.assertEqual(ordered_nodes[0], node_D)
        
        # C cycle shouldn't prevent A and B from being processed as much as possible
        expected_length = 3
        self.assertLessEqual(len(ordered_nodes), expected_length)

if __name__ == '__main__':
    unittest.main()