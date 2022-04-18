RED = True
BLACK = False
# A implementação a seguir é baseada na que está disponível no capítulo 13 da
# segunda edição de Introduction to Algorithms de Cormen et al
class CurrentHeapNull:
    def __init__(self):
        self.parent = None
        self.left = None
        self.right = None
        self.min = None
        self.color = BLACK
        self.is_leaf = True

    def is_black(self):
        return True

    def is_red(self):
        return False

class CurrentHeapNode:
    def __init__(self, key, min, parent, left, right, color):
        self.key = key
        self.min = min
        self.parent = parent
        self.left = left
        self.right = right
        self.color = color
        self.is_leaf = False

    def set_color(self, color):
        self.color = color

    def is_red(self):
        return self.color

    def is_black(self):
        return not self.color

class CurrentHeapRedBlackBST:
    def __init__(self):
        self.null = CurrentHeapNull()
        self.root = self.null

    def is_root(self, node):
        return node is self.root

    def min(self):
        if self.root is None:
            return None
        return self.root.min

    def _search_node(self, node, key):
        if node is self.null or node.key == key:
            return node
        if key < node.key:
            return self._search_node(node.left, key)
        return self._search_node(node.right, key)

    def _min_node(self, node):
        if node.left is self.null:
            return node
        return self._min_node(node.left)

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        x.right.parent = x                                         #       |                  |
        y.parent = x.parent                                        #       x                  y
        if self.is_root(x):                                        #        \  ---------->   /
            self.root = y                                          #         y              x
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        y.min = x.min

    def rotate_right(self, x):
        y = x.left
        if y.right is not self.null:
            x.min = y.right.min
        else:
            x.min = x.key
        x.left = y.right
        x.left.parent = x
        y.parent = x.parent
        if self.is_root(x):
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y


    def insert(self, key):
        if self.root is self.null:
            self.root = CurrentHeapNode(key, key, self.null, self.null,
                                        self.null, BLACK)
            return
        self._insert(self.root, key)

    def _insert(self, node, key):
        parent = node.parent
        current_node = node
        while not current_node.is_leaf:
            parent = current_node
            if key < current_node.key:
                current_node.min = min(current_node.min, key)
                current_node = current_node.left
            else:
                current_node = current_node.right

        new_node = CurrentHeapNode(key, key, parent, self.null, self.null, RED)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._red_black_insert_fix_up(new_node)

    def _red_black_insert_fix_up(self, node):
        while node.parent.is_red():
            parent = node.parent
            grandparent = node.parent.parent
            if parent is grandparent.left:
                uncle = grandparent.right
                if uncle.is_red():
                    grandparent.set_color(RED)
                    parent.set_color(BLACK)
                    uncle.set_color(BLACK)
                    node = grandparent
                else:
                    if node is parent.right:
                        node = parent
                        self.rotate_left(node)
                        parent = node.parent
                        grandparent = node.parent.parent
                    grandparent.set_color(RED)
                    parent.set_color(BLACK)
                    self.rotate_right(grandparent)
            else:
                uncle = grandparent.left
                if uncle.is_red():
                    grandparent.set_color(RED)
                    parent.set_color(BLACK)
                    uncle.set_color(BLACK)
                    node = grandparent
                else:
                    if node is parent.left:
                        node = parent
                        self.rotate_right(node)
                        parent = node.parent
                        grandparent = node.parent.parent
                    grandparent.set_color(RED)
                    parent.set_color(BLACK)
                    self.rotate_left(grandparent)
        self.root.set_color(BLACK)

    def delete(self, key):
        node_with_key_to_be_removed = self._search_node(self.root, key)

        if (node_with_key_to_be_removed.left is self.null
            or node_with_key_to_be_removed.right is self.null):
            node_to_be_removed = node_with_key_to_be_removed
        else:
            node_to_be_removed = self._min_node(node_with_key_to_be_removed.right)

        if node_to_be_removed.left is not self.null:
            substitute = node_to_be_removed.left
        else:
            substitute = node_to_be_removed.right

        substitute.parent = node_to_be_removed.parent
        if self.is_root(node_to_be_removed):
            self.root = substitute
        elif node_to_be_removed is node_to_be_removed.parent.left:
            node_to_be_removed.parent.left = substitute
        else:
            node_to_be_removed.parent.right = substitute

        if node_to_be_removed is not node_with_key_to_be_removed:
            node_with_key_to_be_removed.key = node_to_be_removed.key

        x = substitute
        if x is self.null:
            x = x.parent
            if x is not self.null and substitute is x.left:
                x.min = x.key
        if x is not self.null:
            self.fix_up_attributes(x)

        if node_to_be_removed.is_black():
            self.red_black_delete_fix_up(substitute)

    def fix_up_attributes(self, node):
        child = node
        current_node = child.parent
        while current_node is not self.null:
            if child is current_node.left:
                current_node.min = child.min
            child = current_node
            current_node = current_node.parent

    def red_black_delete_fix_up(self, node):
        while not self.is_root(node) and node.is_black():
            parent = node.parent
            if node is parent.left:
                sibling = parent.right
                if sibling.is_red():
                    sibling.set_color(BLACK)
                    parent.set_color(RED)
                    self.rotate_left(parent)
                    sibling = parent.right

                if sibling.left.is_black() and sibling.right.is_black():
                    sibling.set_color(RED)
                    node = parent
                else:
                    if sibling.right.is_black():
                        sibling.left.set_color(BLACK)
                        sibling.set_color(RED)
                        self.rotate_right(sibling)
                        sibling = parent.right # tem que mudar parent?

                    sibling.set_color(parent.color)
                    parent.set_color(BLACK)
                    sibling.right.set_color(BLACK)
                    self.rotate_left(parent)
                    node = self.root
            else:
                sibling = parent.left
                if sibling.is_red():
                    sibling.set_color(BLACK)
                    parent.set_color(RED)
                    self.rotate_right(parent)
                    sibling = parent.left

                if sibling.left.is_black() and sibling.right.is_black():
                    sibling.set_color(RED)
                    node = parent
                else:
                    if sibling.left.is_black():
                        sibling.right.set_color(BLACK)
                        sibling.set_color(RED)
                        self.rotate_left(sibling)
                        sibling = parent.left

                    sibling.set_color(parent.color)
                    parent.set_color(BLACK)
                    sibling.left.set_color(BLACK)
                    self.rotate_right(parent)
                    node = self.root

        if node is not self.null:
            node.set_color(BLACK)

    def print_heap(self):
        self._print_heap(self.root)

    def _print_heap(self, node):
        if not node.is_leaf:
            self._print_heap(node.left)
            print(node.key, end=' ')
            self._print_heap(node.right)

    def debug_red_black(self):
        if self.root_is_red():
            print("Raiz vermelha")
        if self.red_node_with_red_child():
            print("Nó vermelho com algum filho vermelho")
        if not self.black_height_unique():
            print("Altura negra não bem definida")
        if self.red_leaves():
            print("Há folha vermelhas")

    def root_is_red(self):
        return self.root.is_red()

    def red_node_with_red_child(self):
        return self._red_node_with_red_child(self.root)

    def _red_node_with_red_child(self, node):
        if node.is_leaf:
            return False
        if node.is_red() and (node.left.is_red() or node.right.is_red()):
            return True
        return (self._red_node_with_red_child(node.left)
                or self._red_node_with_red_child(node.right))

    def _downward_black_paths_to_leaves(self, node):
        if node.is_leaf:
            return [[]]
        left_downward_black_paths_to_leaves = self._downward_black_paths_to_leaves(node.left)
        if node.left.is_black():
            for path in left_downward_black_paths_to_leaves:
                path.append(node.left)
        right_downward_black_paths_to_leaves = self._downward_black_paths_to_leaves(node.right)
        if node.right.is_black():
            for path in right_downward_black_paths_to_leaves:
                path.append(node.right)
        return left_downward_black_paths_to_leaves + right_downward_black_paths_to_leaves

    def black_height_unique(self):
        downward_black_paths_to_leaves = self._downward_black_paths_to_leaves(self.root)
        black_height = len(downward_black_paths_to_leaves[0])
        for path in downward_black_paths_to_leaves[1:]:
            if len(path) != black_height:
                return False
        return True

    def red_leaves(self):
        return self._red_leaves(self.root)

    def _red_leaves(self, node):
        if node.is_leaf:
            return False
        if node.is_red() and (node.left is None or node.right is None):
            return True
        return self._red_leaves(node.left) or self._red_leaves(node.right)

    def print(self):
        # a impressão de um nó tem formato chave : prioridade
        self.display()

    # Os métodos display e _display_aux, para impressão das árvores foram obtidos em
    # https://stackoverflow.com/a/54074933
    def display(self):
        if self.root is self.null:
            print()
            return
        lines, *_ = self._display_aux(self.root)
        for line in lines:
            print(line)

    def _display_aux(self, node):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if node.right is self.null and node.left is self.null:
            line = '%s:%s' % (node.key, node.min)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if node.right is self.null:
            lines, n, p, x = self._display_aux(node.left)
            s = '%s:%s' % (node.key, node.min)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if node.left is self.null:
            lines, n, p, x = self._display_aux(node.right)
            s = '%s:%s' % (node.key, node.min)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self._display_aux(node.left)
        right, m, q, y = self._display_aux(node.right)
        s = '%s:%s' % (node.key, node.min)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2
