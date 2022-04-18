import SplayTree as st

class EulerSequence:
    # Essa classe implementa uma sequência euleriana de uma árvore como
    # uma árvore binária com chaves implícitas. A ordem da sequência é a 
    # sequência dos nós em in ordem.
    # Sempre que um novo nó está na raiz da árvore que implementa a sequência,
    # mudamos o atributo euler_sequence desse nó para a sequência em que ele está
    # A raiz é o único nó cujo atributo euler_sequence certamente está atualizado
    def __init__(self, tree):
        self.tree = tree

    @classmethod
    def make_euler_sequence(cls, vertex):
        tree, node = st.SplayTree.make_tree(vertex, vertex)
        euler_seq = EulerSequence(tree)
        node.euler_sequence = euler_seq
        return euler_seq, node

    @classmethod
    def make_from_pair(cls, v, w):
        tree, node = st.SplayTree.make_tree(v, w)
        euler_seq = EulerSequence(tree)
        euler_seq.tree.root.euler_sequence = euler_seq
        return euler_seq, node

    def order(self, x):
        rank = self.tree.order(x)
        self.tree.root.euler_sequence = self
        return rank

    def slice(self, k):
        if k <= 0:
            return None, self
        if k + 1 > self.tree.root.size:
            return self, None

        node = self.tree.search(k)
        first, second = self.tree.split(node)

        first = EulerSequence(first)
        first.tree.root.euler_sequence = first

        second = EulerSequence(second)
        second.tree.root.euler_sequence = second

        return first, second

    def concatenate(self, r):
        if r is None:
            return self

        self.tree.join(r.tree)
        self.tree.root.euler_sequence = self
        return self
