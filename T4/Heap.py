import OperationsRedBlackBST as rb
import CurrentHeapRedBlackBST as ch
import math

class Heap:
    def __init__(self):
        self.current_heap = ch.CurrentHeapRedBlackBST() # árvore rubro negra que guarda as chaves do heap atual
        self.operation_tree = rb.OperationRedBlackBST() # árvore rubro negra que guarda as operações que foram feitas
        self.operation_tree.insert(-math.inf, 0, math.inf)
        self.operation_tree.insert(math.inf, 0, math.inf)

    def insert_insert(self, time, value):
        in_heap = self.operation_tree.insert_insertion(time, value)
        self.current_heap.insert(in_heap)

    def delete_delete(self, time):
        in_heap = self.operation_tree.delete_deletion(time)
        self.current_heap.insert(in_heap)

    def insert_delete(self, time):
        out_heap = self.operation_tree.insert_deletion(time)
        self.current_heap.delete(out_heap)

    def delete_insert(self, time):
        out_heap = self.operation_tree.delete_insertion(time)
        self.current_heap.delete(out_heap)

    def min(self):
        return self.current_heap.min()

    def print(self):
        self.current_heap.print_heap()
        print()