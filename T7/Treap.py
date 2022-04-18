import random
import math

# A implementação que fiz da treap foi baseada na implementação das árvores
# rubro negra sugerida por CLRS em na segunda edição de Introduction to 
# Algorithms. Assim, minha treap conta com nós internos da classe Node e 
# um nó que é pai da raiz da classe RootParent e folhas da classe Leaf.
# As prioridades seguem a propriedade de um maxheap, ie, as prioridades
# dos filhos de um nó são menores que a prioridade daquele nó. Assim,
# o objetos de RootParent têm prioridade infininta, enquanto objetos da
# classe Leaf têm prioridade menos infinito. Além disso, objetos dessas duas
# classes têm campos key, parent, left, right, para facilitar a implementação
# e evitar tratamento explícito de corner cases

class Node:
    def __init__(self, key, parent, left, right):
        self.key = key
        self.priority = random.random()
        self.parent = parent
        self.left = left
        self.right = right

class RootParent:
    def __init__(self):
        self.key = None
        self.priority = math.inf
        self.parent = None
        self.left = None
        self.right = None

class Leaf:
    def __init__(self):
        self.key = None
        self.priority = -math.inf
        self.parent = None
        self.left = None
        self.right = None

class Treap:
    def __init__(self):
        self.root_parent = RootParent()
        self.leaf = Leaf()
        self.root = self.leaf
        self.node_count = 0

    def rotate_left(self, x):
        y = x.right

        x.right = y.left
        x.right.parent = x

        y.left = x
        y.parent = x.parent

        if x is self.root:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        x.parent = y
        self.node_count += 3 # contabilizando acesso a y, y.left e x.parent (supondo aqui já contabilizado o acesso a x)

    def rotate_right(self, x):
        y = x.left

        x.left = y.right
        x.left.parent = x

        y.right = x
        y.parent = x.parent

        if x is self.root:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        x.parent = y
        self.node_count += 3

    def rise(self, node):
        self.node_count += 1 # acesso a node
        while node.parent.priority < node.priority:
            parent = node.parent
            self.node_count += 1 # acesso a node.parent
            if node is parent.left:
                self.rotate_right(parent)
            else:
                self.rotate_left(parent)

    def drop(self, node):
        # em princípio, poderíamos pensar que o algoritmo abaixo não está
        # correto. Afinal, se consideramos apenas uma iteração do loop abaixo
        # quando node tem dois filhos com prioridades maiores que ele, o filho
        # com menor prioridade continua sendo filho de node. Entretanto,
        # a implementaćão que escolhi coloca prioridade menos infinito nas
        # folhas, o que deve fazer com que eventualmente as prioridades fiquem
        # corretas.
        self.node_count += 1 # acesso a node
        while (node.priority < node.left.priority
               or node.priority < node.right.priority):
            self.node_count += 2 # acesso a node.left e node.right
            if node.left.priority < node.right.priority:
                self.rotate_left(node)
            else:
                self.rotate_right(node)

    def _search_node(self, key):
        node = self.root
        while node is not self.leaf:
            self.node_count += 1
            if node.key == key:
                break
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return node

    def search(self, key):
        return self._search_node(key) is not self.leaf

    def min(self):
        if self.root is self.leaf:
            return None

        node = self.root
        while node.left is not self.leaf:
            self.node_count += 1
            node = node.left
        return node.key

    def insert(self, key):
        parent = self.root_parent
        node = self.root
        while node is not self.leaf:
            self.node_count += 1
            parent = node
            if node.key == key:
                return
            if key < node.key:
                node = node.left
            else:
                node = node.right

        new_node = Node(key, parent, self.leaf, self.leaf)
        self.node_count += 1

        if parent is self.root_parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self.rise(new_node)

    def _delete_min(self, root): # remove o mínimo da subárvore enraizada em
        # root e devolve a chave e prioridade do nó que era mínimo
        if root is self.leaf:
            return None, None

        node = root
        while node.left is not self.leaf:
            self.node_count += 1
            node = node.left

        node.right.parent = node.parent
        self.node_count += 1 # acesso a node.right
        if node is self.root:
            self.root = node.right
        elif node is node.parent.left:
            node.parent.left = node.right
        else:
            node.parent.right = node.right
        return node.key, node.priority

    def delete(self, key):
        node = self._search_node(key)
        if node is self.leaf:
            return

        if node.right is self.leaf:
            new_node = node.left
            new_node.parent = node.parent
        elif node.left is self.leaf:
            new_node = node.right
            new_node.parent = node.parent
        else:
            new_key, new_priority = self._delete_min(node.right)
            new_node = Node(new_key, node.parent, node.left, node.right)
            new_node.priority = new_priority
        self.node_count += 3 # o código acima acessa pelo menos node.parent, node.right e node.left

        if node is self.root:
            self.root = new_node
        elif node is node.parent.left:
            node.parent.left = new_node
        else:
            node.parent.right = new_node

        if new_node is not self.leaf:
            self.drop(new_node)

    def print(self):
        # a impressão de um nó tem formato chave : prioridade
        self.display()
        print("Node count = ", self.node_count)

    # Os métodos display e _display_aux, para impressão das árvores foram obtidos em
    # https://stackoverflow.com/a/54074933
    def display(self):
        if self.root is self.leaf:
            print()
            return
        lines, *_ = self._display_aux(self.root)
        for line in lines:
            print(line)

    def _display_aux(self, node):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if node.right is self.leaf and node.left is self.leaf:
            line = '%s : %.5f' % (node.key, node.priority)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if node.right is self.leaf:
            lines, n, p, x = self._display_aux(node.left)
            s = '%s : %.5f' % (node.key, node.priority)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if node.left is self.leaf:
            lines, n, p, x = self._display_aux(node.right)
            s = '%s : %.5f' % (node.key, node.priority)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self._display_aux(node.left)
        right, m, q, y = self._display_aux(node.right)
        s = '%s : %.5f' % (node.key, node.priority)
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



