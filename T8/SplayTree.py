class Pair: 
    # essa classe tem como objetivo guardar um par de números, que é um par de
    # vértices. Se os números são iguais, o par representa um vértice;
    # se não, representa um aresta
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return '(' + str(self.first) + ', ' + str(self.second) + ')'

    def __eq__(self, other):
        return self.first == other.first and self.second == other.second

class Null:
    # essa classe representa um nó nulo e foi criada para evitar tratamento
    # de exceções. Ela servirá como pai da raiz de uma árvore e splay e como folha
    def __init__(self):
        self.value = None
        self.size = 0
        self.parent = None
        self.left = None
        self.right = None

class Node:
    # classe de nós da classe SplayTree. O campo value apontará para um par de 
    # números, size guarda o número de nós da árvore enraizada no nó em questão.
    # Além disso, cada nó conta com um atributo euler_sequence, que aponta para a
    # a sequência euleriana a que o nó (que representa um vértice ou uma aresta)
    # pertence desde que esse nó seja raiz da árvore que representa a sequência eulerina.
    # O atributo hash_position guarda a posição na tabela de hash (da floresta dinâmica
    # em que o nó está) que tem este nó como valor.
    def __init__(self, value, parent, left, right):
        self.value = value
        self.size = left.size + right.size + 1
        self.parent = parent
        self.left = left
        self.right = right
        self.euler_sequence = True
        self.hash_position = -1 # posição na tabela de hash que tem este nó como valor

    def find_root(self):
        # Esse método devolve a raiz da árvore em que o nó está.
        # Estou fazendo dessa maneira, ao invés de fazer como método das splay,
        # porque fazendo como método da splay já teríamos que ter a splay em mãos,
        # o que não faria sentido.
        node = self
        while node.parent.value is not None:
            node = node.parent
        return node

class SplayTree:
    root_parent = Null()
    leaf = root_parent
    # Colocar root_parent e leaf como atributos de classe facilita as operações
    # join e split. Se fossem atributos de instância, teríamos que 
    # atualizar todas as folhas quando ocorresse join

    def __init__(self, root):
        self.root = root

    @classmethod
    def make_tree(cls, first, second):
        root = Node(Pair(first, second), SplayTree.root_parent, SplayTree.leaf,
                    SplayTree.leaf)
        return cls(root), root

    @classmethod
    def from_node(cls, root):
        root.parent = SplayTree.root_parent
        return cls(root)

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        x.right.parent = x

        y.left = x
        y.parent = x.parent

        if x.parent is self.root_parent:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        x.parent = y

        y.size = x.size
        x.size = x.left.size + x.right.size + 1

    def rotate_right(self, x):
        y = x.left

        x.left = y.right
        x.left.parent = x

        y.right = x
        y.parent = x.parent

        if x.parent is self.root_parent:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        x.parent = y
        
        y.size = x.size
        x.size = x.left.size + x.right.size + 1

    def right_right_splay_step(self, x):
        self.rotate_right(x.parent.parent)
        self.rotate_right(x.parent)

    def left_right_splay_step(self, x):
        self.rotate_left(x.parent)
        self.rotate_right(x.parent)

    def left_left_splay_step(self, x):
        self.rotate_left(x.parent.parent)
        self.rotate_left(x.parent)

    def right_left_splay_step(self, x):
        self.rotate_right(x.parent)
        self.rotate_left(x.parent)

    def splay(self, node):
        while node is not self.root:
            parent = node.parent
            grandparent = parent.parent
            if grandparent is self.root_parent:
                if node is parent.left:
                    self.rotate_right(parent)
                else:
                    self.rotate_left(parent)
            else:
                if node is parent.left and parent is grandparent.left:
                    self.right_right_splay_step(node)
                elif node is parent.right and parent is grandparent.left:
                    self.left_right_splay_step(node)
                elif node is parent.right and parent is grandparent.right:
                    self.left_left_splay_step(node)
                else:
                    self.right_left_splay_step(node)

    def splay_max(self):
        node = self.root
        while node.right is not self.leaf:
            node = node.right

        self.splay(node)

    def join(self, t):
        # Junta a árvore t na árvore self "depois" de self
        self.splay_max()
        self.root.right = t.root
        self.root.right.parent = self.root
        self.root.size = self.root.left.size + self.root.right.size + 1
        
    def split(self, x):
        self.splay(x)

        new_root = x.right
        new_tree = SplayTree.from_node(new_root)

        x.right = SplayTree.leaf
        x.size = x.left.size + 1
        return self, new_tree

    def search(self, k):
        if k > self.root.size or k <= 0:
            return

        node = self.root
        while True:
            if k == node.left.size + 1:
                break
            elif k > node.left.size + 1:
                k -= node.left.size + 1
                node = node.right
            else:
                node = node.left

        self.splay(node)
        return node

    def order(self, x):
        self.splay(x)
        return x.left.size + 1 # x agora é raiz
   
    def print(self):
        # a impressão de um nó tem formato chave : prioridade
        self.display()

    # Os métodos display e _display_aux, para impressão das árvores foram obtidos em
    # https://stackoverflow.com/a/54074933
    def display(self):
        lines, *_ = self._display_aux(self.root)
        for line in lines:
            print(line)

    def _display_aux(self, node):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if node.right is self.leaf and node.left is self.leaf:
            line = str(node.value)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if node.right is self.leaf:
            lines, n, p, x = self._display_aux(node.left)
            s = str(node.value)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if node.left is self.leaf:
            lines, n, p, x = self._display_aux(node.right)
            s = str(node.value)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self._display_aux(node.left)
        right, m, q, y = self._display_aux(node.right)
        s = str(node.value)
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


