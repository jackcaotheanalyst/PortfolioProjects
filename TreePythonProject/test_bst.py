import unittest
from Trees.src.trees.bst_tree import BST
from Trees.src.nodes.bst_node import BSTNode


class TestBST(unittest.TestCase):
    def test_create_empty_tree(self):
        tree = BST()
        self.assertEqual(len(tree), 0)
        self.assertIsNone(tree.root)

    def test_add_value(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(99)
        tree.add_value(101)
        self.assertEqual(100, tree.root.value)
        self.assertEqual(99, tree.root.left.value)
        self.assertEqual(101, tree.root.right.value)

    def test_add_value2(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(80)
        tree.add_value(200)
        tree.add_value(90)
        tree.add_value(70)
        self.assertEqual(90, tree.root.left.right.value)

    def test_height(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(99)
        tree.add_value(101)
        self.assertEqual(1, tree.height)

    def test_get_node(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(99)
        tree.add_value(101)
        self.assertEqual(tree.root, tree.get_node(100))
        self.assertEqual(tree.root.right, tree.get_node(101))
        self.assertEqual(tree.root.left, tree.get_node(99))

    def test_get_max_node(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(80)
        tree.add_value(200)
        tree.add_value(90)
        tree.add_value(70)
        self.assertEqual(tree.root.right, tree.get_max_node())

    def test_get_min_node(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(80)
        tree.add_value(200)
        tree.add_value(90)
        tree.add_value(70)
        self.assertEqual(tree.root.left.left, tree.get_min_node())

    def test_remove_value(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(80)
        tree.add_value(200)
        tree.add_value(90)
        tree.add_value(70)
        tree.remove_value(70)
        tree.remove_value(90)
        self.assertEqual(None, tree.get_node(80).left)
        self.assertEqual(None, tree.get_node(80).right)

    def test_remove_value2(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(80)
        tree.add_value(200)
        tree.add_value(90)
        tree.add_value(70)
        tree.remove_value(70)
        tree.remove_value(90)
        tree.remove_value(80)
        tree.remove_value(200)
        self.assertEqual(None, tree.get_node(100).left)
        self.assertEqual(None, tree.get_node(100).right)

    def test_remove_value3(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(80)
        tree.add_value(200)
        tree.add_value(90)
        tree.add_value(70)
        tree.remove_value(80)
        self.assertEqual(70, tree.get_node(100).left.value)

    def test_remove_value4(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(80)
        tree.add_value(200)
        tree.add_value(90)
        tree.add_value(70)
        tree.remove_value(100)
        self.assertEqual(90, tree.root.value)
        self.assertEqual(80, tree.root.left.value)
        self.assertEqual(70, tree.root.left.left.value)

    def test_remove_value5(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(80)
        tree.add_value(200)
        tree.add_value(90)
        tree.add_value(70)
        tree.remove_value(100)
        tree.remove_value(80)
        self.assertEqual(90, tree.root.value)
        self.assertEqual(70, tree.root.left.value)

    def test_remove_value6(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(80)
        tree.add_value(200)
        tree.add_value(90)
        tree.add_value(70)
        tree.add_value(150)
        tree.add_value(250)
        tree.remove_value(200)
        self.assertEqual(150, tree.root.right.value)
        tree.remove_value(150)
        self.assertEqual(250, tree.root.right.value)

    def test_create_tree(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(80)
        tree.add_value(200)
        tree.add_value(90)
        tree.add_value(70)

        root = BSTNode(100)
        root.left = BSTNode(80)
        root.right = BSTNode(200)
        root.left.left = BSTNode(70)
        root.left.right = BSTNode(90)

        cmp_tree = BST(root)
        self.assertEqual(tree, cmp_tree)

    def test_tree_not_eq(self):
        tree = BST()
        tree.add_value(100)
        tree.add_value(80)
        tree.add_value(200)
        tree.add_value(90)
        tree.add_value(70)

        root = BSTNode(100)
        root.left = BSTNode(80)
        root.right = BSTNode(200)
        root.left.left = BSTNode(70)
        root.left.right = BSTNode(92)

        cmp_tree = BST(root)
        cmp_tree._num_nodes = 5
        self.assertNotEqual(tree, cmp_tree)

    def test_string_tree(self):
        tree = BST(key=lambda x: len(x))
        tree.add_value('a')
        tree.add_value('ab')
        tree.add_value('')
        tree.add_value('cat')
        tree.add_value('apples')
        self.assertEqual('a', tree.root.value)
        self.assertEqual('', tree.root.left.value)
        self.assertEqual('ab', tree.root.right.value)
        self.assertEqual('cat', tree.root.right.right.value)
        self.assertEqual(3, tree.key(tree.root.right.right.value))
        self.assertEqual(5, len(tree))
        self.assertEqual(3, tree.height)
        self.assertEqual('ab', tree.get_node(tree.key('ab')).value)
        self.assertEqual('apples', tree.get_node(tree.key('apples')).value)


if __name__ == '__main__':
    unittest.main()
