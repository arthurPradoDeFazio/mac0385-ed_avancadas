import RedBlackBST as rb

class Stack:
    # A pilha será representada por uma árvore rubro-negra cujas operações 
    # estão armazenadas nas folhas. Mais detalhes sobre a implementação dessa
    # árvore estão em RedBlackBST.py
    def __init__(self):
        self.bst = rb.RedBlackBST()

    def push(self, time, value):
        self.bst.insert(time, 1, value)

    def pop(self, time):
        self.bst.insert(time, -1, None)

    def delete_operation(self, time):
        self.bst.delete(time)

    def delete_push(self, time):
        self.bst.delete(time)

    def delete_pop(self, time):
        self.bst.delete(time)

    def top(self, time):
        return self.bst.top(time)

    def kth(self, time, k):
        return self.bst.kth(time, k)

    def size(self, time):
        return self.bst.weight_up_to(time)

    def print(self, time):
        leaves = self.bst.find_leaves_up_to(time)
        k = 0
        for i in range(len(leaves) - 1, -1, -1):
            if leaves[i].operation == -1:
                k += 1
            else:
                if k == 0:
                    print(leaves[i].value, end=' ')
                else:
                    k -= 1
        print()
