import EulerSequence as es
import Treap as treap

class HashNode:
    def __init__(self, key, value):
        # A chave armazenada da aresta v-w é v * n + w e value aponta para
        # um dos nós na sequência euleriana que tem v-w como value
        self.key = key
        self.value = value

    def __hash__(self):
        return self.key

class HashTable:
    # Tabela de Hash implementada com Linear Probbing
    # A implementação foi obtida no livro do Sedgewick
    def __init__(self, capacity=16):
        self.size = 0 # número de pares chave valor a serem inseridos
        self.capacity = capacity # capacidade máxima de nós chaves-valor
        self.table = [None] * self.capacity

    def hashf(self, x):
        return hash(x) % self.capacity 

    def put(self, hash_node):
        if self.size >= self.capacity // 2:
            self.resize(2 * self.capacity)

        i = self.hashf(hash_node)
        while self.table[i] is not None:
            i = (i + 1) % self.capacity

        self.table[i] = hash_node
        self.table[i].value.hash_position = i
        self.size += 1

    def resize(self, new_capacity):
        new_ht = HashTable(new_capacity)
        for i in range(0, self.capacity):
            if self.table[i] is not None:
                new_ht.put(self.table[i])

        self.capacity = new_capacity
        self.table = new_ht.table

    def get(self, key):
        i = self.hashf(key)
        while self.table[i] is not None:
            if key == self.table[i].key:
                return self.table[i]
            i = (i + 1) % self.capacity
        return None

    def delete(self, key):
        i = self.hashf(key)
        while self.table[i].key != key:
            i = (i + 1) % self.capacity
        self.table[i].value.hash_position = -1
        self.table[i] = None

        i = (i + 1) % self.capacity
        while self.table[i] is not None:
            node = self.table[i]
            self.table[i] = None
            self.size -= 1
            self.put(node)
            i = (i + 1) % self.capacity

        self.size -= 1
        if self.size <= self.capacity // 8:
            self.resize(self.capacity // 2)

    def delete_index(self, i):
        self.table[i].value.hash_position = -1
        self.table[i] = None

        i = (i + 1) % self.capacity
        while self.table[i] is not None:
            node = self.table[i]
            self.table[i] = None
            self.size -= 1
            self.put(node)
            i = (i + 1) % self.capacity

        self.size -= 1
        if self.size <= self.capacity // 8:
            self.resize(self.capacity // 2)


class DynamicForest:
    def __init__(self, n):
        self.n = n
        self.hash_table = HashTable()
        self.edges = treap.Treap() # guarda as chaves que identificam todas as arestas presentes na floresta
                                   # as arestas são guardadas sempre na forma v * n + w, com v < w

        for v in range(0, n):
            key = v * n + v
            _, value = es.EulerSequence.make_euler_sequence(v)
            self.hash_table.put(HashNode(key, value))

    def find(self, node):
        return node.find_root().euler_sequence

    def get(self, v, w):
        node = self.hash_table.get(v * self.n + w)
        if node is None:
            return None
        return node.value

    def connected(self, v, w):
        v_tree_node = self.get(v, v)
        w_tree_node = self.get(w, w)
        v_sequence = self.find(v_tree_node)
        w_sequence = self.find(w_tree_node)
        return v_sequence is w_sequence

    def bring_to_front(self, v):
        v_node = self.get(v, v)
        v_sequence = self.find(v_node) # s: rr rx ... wv vv ... vv vw ww ... rr -> r: raiz, w: algum vértice adjacente a v
        v_position_sequence = v_sequence.order(v_node) # não temos a garantia de que v_node é a primeira ocorrência de v na sequência, mas tudo bem

        if v_position_sequence == 1: # v já está na frente, não precisa fazer mais nada
            return v_sequence

        before_v, from_v = v_sequence.slice(v_position_sequence - 1) # v_position_sequence >= 2 por conta do if acima. before_v: rr rx ... wv, from_v: vv ... vv vw ww ... rr
        current_root_seq, before_v = before_v.slice(1) # current_root = rr, before_v: rx ... wv

        current_root_node = current_root_seq.tree.root
        self.hash_table.delete_index(current_root_node.hash_position)

        vv_sequence, vv_tree_node = es.EulerSequence.make_euler_sequence(v)
        self.hash_table.put(HashNode(v * self.n + v, vv_tree_node))

        _ = from_v.concatenate(before_v) # from_v: vv ... vv vw ww ... rr rx ... wv
        return from_v.concatenate(vv_sequence) # from_v: vv ... vv vw ww ... rr rx ... wv vv -> não importa se não pegamos a primeira ocorrência de v

    def cut(self, v, w):
        if self.get(v, w) is None:
            return

        self.remove_edge(v, w)

        s = self.bring_to_front(v) # s: vv ... vv vw ww ... ww wv vv ... vv
        vw_node = self.get(v, w)
        wv_node = self.get(w, v)
        vw_sequence_position = s.order(vw_node)
        wv_sequence_position = s.order(wv_node)

        v_to_w, after_w = s.slice(wv_sequence_position - 1) # v_to_w: vv ... vv vw ww ... ww, after_w: wv vv va ... vv
        v_to_v, w_tree = v_to_w.slice(vw_sequence_position - 1) # v_to_v: vv ... vv, w_tree: vw ww ... ww
        vw, w_tree = w_tree.slice(1) # w_tree: ww ... ww
        wv_vv, after_w = after_w.slice(2) # after_w: va ... vv
        wv, vv = wv_vv.slice(1)
        if v_to_v is not None: # caso em que s: vv vw ww ... ww wv vv ... vv implica v_to_v = None na linha 141
            _ = v_to_v.concatenate(after_w)

        self.hash_table.delete_index(vw_node.hash_position)
        self.hash_table.delete_index(wv_node.hash_position)
        vv_node_to_delete = vv.tree.root
        self.hash_table.delete_index(vv_node_to_delete.hash_position)
        

    def link(self, v, w):
        if self.connected(v, w):
            return

        self.add_edge(v, w)

        s = self.bring_to_front(v) # s: vv ... vv
        r = self.bring_to_front(w) # r: ww ... ww

        vw_euler_sequence, vw_node = es.EulerSequence.make_from_pair(v, w) # vw_euler_sequence: vw
        self.hash_table.put(HashNode(v * self.n + w, vw_node))

        wv_euler_sequence, wv_node = es.EulerSequence.make_from_pair(w, v) # wv_euler_sequence: wv
        self.hash_table.put(HashNode(w * self.n + v, wv_node))

        vv_euler_sequence, vv_node = es.EulerSequence.make_from_pair(v, v) # vv_euler_sequence: vv
        self.hash_table.put(HashNode(v * self.n + v, vv_node))

        _ = s.concatenate(vw_euler_sequence) # s: vv ... vv vw
        _ = s.concatenate(r)                 # s: vv ... vv vw ww ... ww
        _ = s.concatenate(wv_euler_sequence) # s: vv ... vv vw ww ... ww wv
        _ = s.concatenate(vv_euler_sequence) # s: vv ... vv vw ww ... ww wv vv

    def add_edge(self, v, w):
        if v > w:
            v, w = w, v
        self.edges.insert(v * self.n + w)

    def remove_edge(self, v, w):
        if v > w:
            v, w = w, v
        self.edges.delete(v * self.n + w)

    def print(self):
        self._print(self.edges.root)

    def _print(self, node):
        if node is self.edges.leaf:
            return

        self._print(node.left)
        v = node.key // self.n
        w = node.key % self.n
        print(v, "-", w)
        self._print(node.right)




        


