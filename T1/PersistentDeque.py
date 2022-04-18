# Arthur Prado De Fazio
# NUSP: 9298614
# Esta implementação foi fortemente baseada no pseudo-código disponível
# na tese de mestrado de Yan Couto

import Node as nd

class Deque:
    def __init__(self, first=None, last=None):
        if first is None:
            first = nd.Node()
            last = first
        self.first = first
        self.last = last

    def swap(self):
        return Deque(self.last, self.first)

    def push_front(self, val):
        node = nd.Node(self.first, self.first.depth + 1, val)
        if self.first.depth == 0:
            return Deque(node, node)
        return Deque(node, self.last)

    def push_back(self, val):
        return self.swap().push_front(val).swap()

    def pop_front(self):
        if self.first is self.last:
            return Deque()
        elif self.first.lowest_common_ancestor(self.last) is self.first:
            return Deque(self.last.level_ancestor(self.last.depth - self.first.depth - 1), self.last)
        return Deque(self.first.parent, self.last)

    def pop_back(self):
        return self.swap().pop_front().swap()

    def front(self):
        return self.first.val

    def back(self):
        return self.last.val

    def kth(self, k):
        if self.first.val is None:
            print("Erro! Deque vazia!")
            return
        mid = self.first.lowest_common_ancestor(self.last)
        l1 = self.first.depth - mid.depth
        l2 = self.last.depth - mid.depth
        if k <= 0 or k - 1 > l1 + l2:
            print("Erro, não há", k, "-ésimo elemento")
            return
        if k - 1 <= l1:
            return self.first.level_ancestor(k - 1).val
        return self.last.level_ancestor(l2 + l1 + 1 - k).val

    def print(self):
        if self.first.depth == 0:
            print("\n", end = '')
            return
        mid = self.first.lowest_common_ancestor(self.last)
        node = self.first
        while node is not mid:
            print(node.val, end = ' ')
            node = node.parent
        node = self.last
        second_half = []
        while node is not mid:
            second_half.append(node.val)
            node = node.parent
        second_half.append(mid.val)
        for val in reversed(second_half):
            print(val, end = ' ')
        print("\n", end = '')
