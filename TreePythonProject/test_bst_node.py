import unittest
from Trees.src.nodes.bst_node import BSTNode


class TestBSTNode(unittest.TestCase):
    def test_node(self):
        root = BSTNode(100)
        self.assertEqual(100, root.value)
        left = BSTNode(90)
        root.left = left
        self.assertEqual(90, root.left.value)
        right = BSTNode(110)
        right.parent = root
        self.assertEqual(100, right.parent.value)


if __name__ == '__main__':
    unittest.main()
