import copy
from typing import Optional, Callable, TypeVar, Generic, Dict

from Trees.src.errors import MissingValueError, EmptyTreeError
from Trees.src.nodes.bst_node import BSTNode

T = TypeVar('T')
K = TypeVar('K')


class BST(Generic[T, K]):
    """
    T: The value stored in the node
    K: The value used in comparing nodes
    """

    def __init__(self, root: Optional[BSTNode[T]] = None, key: Callable[[T], K] = lambda x: x) -> None:
        """
        You must have at least one member named root

        :param root: The root node of the tree if there is one.
        If you are provided a root node don't forget to count how many nodes are in it
        :param key: The function to be applied to a node's value for comparison purposes.
        It serves the same role as the key function in the min, max, and sorted builtin
        functions
        """
        self.root = root
        self.key = key

    @property
    def height(self) -> int:
        """
        Compute the height of the tree. If the tree is empty its height is -1
        :return:
        """
        if self.root is None:
            return -1
        else:
            return self._height(-1, self.root)

    def _height(self, current_height: int, current_node: Optional[BSTNode[T]] = None) -> int:
        if current_node is None:
            return current_height
        else:
            left_height = self._height(current_height + 1, current_node.left)
            right_height = self._height(current_height + 1, current_node.right)
            return max(left_height, right_height)

    def __len__(self) -> int:
        """
        :return: the number of nodes in the tree
        """
        if self.root is None:
            return 0
        else:
            return self.get_size(self.root)

    def get_size(self, current_node: Optional[BSTNode[T]] = None) -> int:
        if current_node is None:
            return 0
        else:
            return self.get_size(current_node.left) + 1 + self.get_size(current_node.right)

    def add_value(self, value: T) -> None:
        """
        Add value to this BST
        Duplicate values should be placed on the right
        :param value:
        :return:
        """
        if self.root is None:  # found the spot to add the node
            self.root = BSTNode(value)
        else:
            self._add_value(value, self.root)

    def _add_value(self, value: T, current_node: Optional[BSTNode[T]] = None) -> None:
        key_value = self.key(value)
        if current_node is not None:
            if key_value < self.key(current_node.value):
                if current_node.left is not None:
                    return self._add_value(value, current_node.left)
                else:
                    current_node.left = BSTNode(value)
                    current_node.left.parent = current_node
            else:
                if current_node.right is not None:
                    return self._add_value(value, current_node.right)
                else:
                    current_node.right = BSTNode(value)
                    current_node.right.parent = current_node

    def get_node(self, value: K) -> BSTNode[T]:
        """
        Get the node with the specified value
        :param value:
        :raises MissingValueError if there is no node with the specified value
        :return:
        """
        return self._get_node(value, self.root)

    def _get_node(self, value: K, current_node: Optional[BSTNode[T]] = None) -> BSTNode[T]:
        if current_node is None:
            raise MissingValueError()
        elif value == self.key(current_node.value):
            return current_node
        else:
            if value < self.key(current_node.value):
                return self._get_node(value, current_node.left)
            else:
                return self._get_node(value, current_node.right)

    def get_max_node(self) -> BSTNode[T]:
        """
        Return the node with the largest value in the BST
        :return:
        :raises EmptyTreeError if the tree is empty
        """
        if self.root is None:
            raise EmptyTreeError()
        else:
            return self._get_max_node(self.root)

    def _get_max_node(self, current_node: Optional[BSTNode[T]] = None) -> BSTNode[T]:
        if current_node.right is not None:
            return self._get_max_node(current_node.right)
        else:
            return current_node

    def get_min_node(self) -> BSTNode[T]:
        """
        Return the node with the smallest value in the BST
        :return:
        """
        if self.root is None:
            raise EmptyTreeError()
        else:
            return self._get_min_node(self.root)

    def _get_min_node(self, current_node: Optional[BSTNode[T]] = None) -> BSTNode[T]:
        if current_node.left is not None:
            return self._get_min_node(current_node.left)
        else:
            return current_node

    def delete_node(self, node: Optional[BSTNode[T]] = None) -> None:
        if node is not None:
            if node != self.root:
                if node.parent.left == node:
                    node.parent.left.value = None
                    node.parent.left = None
                else:
                    node.parent.right.value = None
                    node.parent.right = None
            else:
                self.root = None

    @staticmethod
    def num_children(node: Optional[BSTNode[T]] = None) -> int:
        if node.left is not None and node.right is not None:
            return 2
        elif node.left is not None or node.right is not None:
            return 1
        else:
            return 0

    def replace_child(self, node: Optional[BSTNode[T]] = None) -> None:
        if node is not None:
            if node.left is not None:
                if node == self.root:
                    self.root.left.parent = None
                    self.root = self.root.left
                else:
                    if node.parent.left == node:
                        node.parent.left = node.left
                        node.left.parent = node.parent
                    else:
                        node.parent.right = node.left
                        node.left.parent = node.parent
            else:
                if node == self.root:
                    self.root.right.parent = None
                    self.root = self.root.right
                else:
                    if node.parent.left == node:
                        node.parent.left = node.right
                        node.right.parent = node.parent
                    else:
                        node.parent.right = node.right
                        node.right.parent = node.parent

    def remove_value(self, value: K) -> None:
        """
        Remove the node with the specified value.
        When removing a node with 2 children take the successor for that node
        to be the largest value smaller than the node (the max of the
        left subtree)
        :param value:
        :return:
        :raises MissingValueError if the node does not exist
        """
        node_to_remove = self.get_node(self.key(value))
        return self._remove_value(node_to_remove)

    def _remove_value(self, node_to_remove: Optional[BSTNode[T]] = None) -> None:
        if BST.num_children(node_to_remove) == 0:
            self.delete_node(node_to_remove)
        elif BST.num_children(node_to_remove) == 1:
            self.replace_child(node_to_remove)
        else:
            successor = self._get_max_node(node_to_remove.left)
            node_to_remove.value = successor.value
            self._remove_value(successor)

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        elif isinstance(other, BST):
            if len(self) == 0 and len(other) == 0:
                return True
            else:
                return len(self) == len(other) and self.root.value == other.root.value and \
                       BST(self.root.left) == BST(other.root.left) and \
                       BST(self.root.right) == BST(other.root.right)
        else:
            return False

    def __ne__(self, other: object) -> bool:
        return not (self == other)

    def __deepcopy__(self, memodict: Dict) -> "BST[T,K]":
        """
        I noticed that for some tests deepcopying didn't
        work correctly until I implemented this method so here
        it is for you
        :param memodict:
        :return:
        """
        new_root = copy.deepcopy(self.root, memodict)
        new_key = copy.deepcopy(self.key, memodict)
        return BST(new_root, new_key)
