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