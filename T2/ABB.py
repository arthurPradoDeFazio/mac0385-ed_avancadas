class Node:
    def __init__(self, key=None, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

    def node_copy(self):
        return Node(self.key, self.left, self.right)

class BST:
    def __init__(self):
        self.root = None

    def search(self, x):
        return self._search(self.root, x)

    def _search(self, node, x):
        if node is None:
            return False
        if node.key == x:
            return True
        if x < node.key:
            return self._search(node.left, x)
        return self._search(node.right, x)

    def insert(self, x):
        if self.search(x):
            return self
        new_tree = BST()
        new_tree.root = new_tree._insert(self.root, x)
        return new_tree

    def _insert(self, node, x):
        if node is None:
            return Node(x, None, None)
        new_node = node.node_copy()
        if x < node.key:
            new_node.left = self._insert(node.left, x)
        else:
            new_node.right = self._insert(node.right, x)
        return new_node

    def min(self):
        if self.root is None:
            return None
        return self._min(self.root)

    def _min(self, node):
        if node.left is None:
            return node.key
        return self._min(node.left)

    def delete_min(self):
        if self.root is None:
            return self
        new_tree = BST()
        new_tree.root = new_tree._delete_min(self.root)
        return new_tree

    def _delete_min(self, node):
        if node.left is None:
            return node.right
        new_node = node.node_copy()
        new_node.left = self._delete_min(node.left)
        return new_node

    def delete(self, x):
        if not self.search(x):
            return self
        new_tree = BST()
        new_tree.root = new_tree._delete(self.root, x)
        return new_tree

    def _delete(self, node, x):
        if node.key == x:
            if node.right is None:
                return node.left
            return Node(self._min(node.right), node.left,
                        self._delete_min(node.right))

        new_node = node.node_copy()
        if x < node.key:
            new_node.left = self._delete(node.left, x)
        else:
            new_node.right = self._delete(node.right, x)
        return new_node

    def print(self):
        if self.root is None:
            print()
            return
        self._print(self.root, 0)

    # A função abaixo foi estudada e obtida em https://www.geeksforgeeks.org/print-binary-tree-2-dimensions/
    def _print(self, node, space):
        if node is None:
            return
        space += 10
        self._print(node.right, space)
        print()
        for i in range(10, space):
            print(end=' ')
        print(node.key)
        self._print(node.left, space)
