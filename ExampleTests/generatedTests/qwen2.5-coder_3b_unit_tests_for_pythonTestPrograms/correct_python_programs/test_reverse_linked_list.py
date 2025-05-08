class TestReverseLinkedList(unittest.TestCase):
    def setUp(self):
        # Define some example linked list nodes for testing
        self.nodes = [1, 2, 3, 4, 5]
        self.head = None

        for num in reversed(self.nodes):
            new_node = ListNode(num)
            if not self.head:
                self.head = new_node
            else:
                new_node.next = self.head
                self.head = new_node

    def test_reverse_linked_list(self):
        # Reverse the linked list and check if it's correct
        reversed_head = reverse_linked_list(self.head)

        current_node = reversed_head
        expected_nodes = self.nodes[::-1]
        for i, expected in enumerate(expected_nodes):
            self.assertEqual(current_node.val, expected)
            current_node = current_node.next

    def test_reverse_linked_list_empty_list(self):
        # Check that reversing an empty list returns None
        head = reverse_linked_list(None)
        self.assertIsNone(head)


if __name__ == "__main__":
    unittest.main()
