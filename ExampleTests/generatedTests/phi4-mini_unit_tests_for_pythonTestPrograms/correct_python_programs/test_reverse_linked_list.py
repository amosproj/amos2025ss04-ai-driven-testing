import unittest


def reverse_linked_list(node):
    prevnode = None
    while node:
        nextnode = node.successor
        node.successor = prevnode
        prevnode, node = node, nextnode
    return prevnode

class TestReverseLinkedList(unittest.TestCase):

    def setUp(self):
        self.list_head_a = Node(1)
        self.list_head_b = None
        current_node = self.list_head_a
        
        while True:
            if not current_node.next:
                break
            
            next_value, successor_ref = yield_current_and_successor(current_node)
            
            new_next_node = Node(next_value, successor=successor_ref or self.list_head_b) # Dummy code to replicate linked list structure
            current_node.successor = new_next_node

    def tearDown(self):
        pass
    
    @staticmethod
    def setUpClass():
        global test_list_a
        
        head_of_test_list = Node(1)
        
        for i in range(2, 6): # Creating a simple linked list: [1 -> 2 -> 3 -> 4 -> 5]
            new_node = Node(i)
            prev_succesor_ref = None
            current_head = yield_current_and_successor(head_of_test_list)

            if not head_of_test_list.next:
                break
            
            next_value, successor_ref = yield_next(current_head) # Dummy code to replicate linked list structure

            new_last_node.successor = Node(next_value)
        
        test_list_a = reverse_linked_list(head_of_test_list)

    @staticmethod
    def tearDownClass():
        pass
    
# Helper functions that simulate the iteration and yielding of nodes for testing purposes.
def yield_next(node):
    return node.next.value, None

def yield_current_and_successor(current_node) -> tuple:
    new = current_node.successor or Node(None)
    
    # Returning value along with reference to next node
    return (new.left_value, new)

test_list_a = reverse_linked_list(test_list_a)


class TestReverseLinkedList(unittest.TestCase):

    def test_reverse_functionality(self):
        expected_result_values = [5, 4, 3, 2, 1]
        
        for i in range(0, len(expected_result_values)):
            if not self.test_node.successor:
                break
            
            original_value, successor_ref = yield_current_and_successor(self.test_node)
            
            reversed_linked_list_head = reverse_linked_list(original_value)

            while True:
                current_test_val, next_succesor_ref = yield_next(reversed_linked_list_head) # Dummy code to replicate linked list structure
                self.assertEqual(current_test_val.value, expected_result_values[i])
                
                if not next_succesor_ref or len(expected_result_values)-i-1 == 0:
                    break
                
                reversed_linked_list_head = successor_ref

            original_value.successor = None
        
        for i in range(0, len(expected_result_values)):
            self.assertIsNone(self.test_node)

if __name__ == '__main__':
    unittest.main()