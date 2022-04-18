class Node:
    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

class SplayTree:
    def __init__(self):
        self.root = None
        self.node_count = 0 # contador do número de nós acessados

    def rotate_left(self, x):
        y = x.right

        x.right = y.left
        if y.left is not None:
            y.left.parent = x                           #       x                       y
                                                        #      / \                     / \
        y.left = x                                      #     a   y     -------->     x   c
        y.parent = x.parent                             #        / \                 / \
                                                        #       b   c               a   b
        if x.parent is None:
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
        if y.right is not None:
            y.right.parent = x                          #      x                      y
                                                        #     / \                    / \
        y.right = x                                     #    y   c  ---------->     a   x
        y.parent = x.parent                             #   / \                        / \
                                                        #  a   b                      b   c
        if x.parent is None:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        x.parent = y
        self.node_count += 3


    def right_right_splay_step(self, x):                  #       z                              x
        # supomos que x tenha avô                         #      / \                            / \
        self.rotate_right(x.parent.parent)                #     y   d         ---------->      a   y
        self.rotate_right(x.parent)                       #    / \                                / \
                                                          #   x   c                              b   z
                                                          #  / \                                    / \
                                                          # a   b                                  c   d
        self.node_count += 2 # estamos contabilizando os acessos a x.parent e x.parent.parent

    def left_right_splay_step(self, x):                   #      z                               x
        # supomos que x tenha avô                         #     / \                             / \
        self.rotate_left(x.parent)                        #    y   d                           /   \
        self.rotate_right(x.parent)                       #   / \           ----------->      y     z
                                                          #  a   x                           / \   / \
                                                          #     / \                         a   b c   d
                                                          #    b   c
        self.node_count += 2

    def left_left_splay_step(self, x):
        # supomos que x tenha avô
        # left_left_splay_step é a operacão simétrica de right_right_splay_step
        # ou seja, partimos de uma situacão em que x é filho direito de seu pai e seu pai é filho direito de
        # seu avô
        self.rotate_left(x.parent.parent)
        self.rotate_left(x.parent)
        self.node_count += 2

    def right_left_splay_step(self, x):
        # supomos que x tenha avô
        # right_left_splay_step é a operaćão simétrica de left_right_splay_step
        # ou seja, partimos de uma situacão na qual x é filho esquerdo de seu pai, que, por sua vez é
        # filho direito de seu pai
        self.rotate_right(x.parent)
        self.rotate_left(x.parent)
        self.node_count += 2

    def splay(self, node):
        while node is not self.root: # => node.parent não é None
            parent = node.parent
            grandparent = node.parent.parent
            self.node_count += 2 # acesso a parent e grandparent
            if grandparent is None:  # node é filho da raiz
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

    def search(self, key):
        if self.root is None:
            return False

        node = self.root
        parent = None
        while node is not None:
            self.node_count += 1
            parent = node
            if node.key == key:
                self.splay(node)
                return True
            if node.key < key:
                node = node.right
            else:
                node = node.left

        if parent is not None:
            # self.node_count += 1 <- acho que não devo colocar esse acréscimo pois ele foi contabilizado quando node foi igual a parent
            self.splay(parent)
        return False

    def insert(self, key):
        if self.search(key):
            return

        node = self.root
        parent = None
        while node is not None:
            self.node_count += 1
            parent = node
            if node.key < key:
                node = node.right
            else:
                node = node.left

        new_node = Node(key, None, None, parent)
        self.node_count += 1
        if parent is None:
            self.root = new_node
        else:
            if key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node
            self.splay(new_node)

    def min(self):
        if self.root is None:
            return None
        self.node_count += 1
        return self._min(self.root)

    def _min(self, node):
        if node.left is None:
            self.splay(node)
            return node.key
        self.node_count += 1
        return self._min(node.left)

    def delete(self, key):
        if not self.search(key):
            return

        # observe que se a busca do if acima foi bem sucedida, então o nó com key encontra-se agora na raiz da árvore
        self.node_count += 1 # acesso a self.root.right
        if self.root.right is None:
            self.root = self.root.left
            self.node_count += 1 # acesso a self.root.left
            if self.root is not None:
                self.root.parent = None
            return

        self.node_count += 1 # acesso a self.root.right abaixo
        _ = self._min(self.root.right) # vamos chamar o valor devolvido por essa chamada de min_right a seguir
        # sabemos que o mínimo da subárvore direita existe, pois self.root.right não é None. Aí, a chamada acima faz com
        # que o mínimo da antiga subárvore direita da raiz esteja na raiz da árvore. Independente da profundidade do nó
        # que tinha min_right como chave, esse nó está na raiz e o nó que possui key como chave é seu filho esquerdo.
        # Temos a seguinte árvore:
        #           min_right
        #           /       \
        #          key       B
        #         /  \
        #        A    None
        # A e B são nós ou None
        self.node_count += 1 # acesso a self.root.right.right
        self.root.left = self.root.left.left
        if self.root.left is not None:
            self.root.left.parent = self.root

    def print(self):
        # não consideramos os acessos feitos nos métodos de impressão para 
        # aumento do node_count
        self.display()
        print("Node count = ", self.node_count)

    # Os métodos display e _display_aux, para impressão das árvores foram obtidos em
    # https://stackoverflow.com/a/54074933
    def display(self):
        if self.root is None:
            print()
            return
        lines, *_ = self._display_aux(self.root)
        for line in lines:
            print(line)

    def _display_aux(self, node):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if node.right is None and node.left is None:
            line = '%s' % node.key
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if node.right is None:
            lines, n, p, x = self._display_aux(node.left)
            s = '%s' % node.key
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if node.left is None:
            lines, n, p, x = self._display_aux(node.right)
            s = '%s' % node.key
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self._display_aux(node.left)
        right, m, q, y = self._display_aux(node.right)
        s = '%s' % node.key
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



