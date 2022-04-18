RED = True
BLACK = False
# As classes a seguir servem para definir a árvore balanceada em que está implementada a
# pilha retroativa. Neste caso utilizamos uma árvore rubro negra. Há dois tipos de
# nós: os da classe InternalNode e os da classe Leaf.
# As operações realizadas na pilha são armazenadas nas folhas, de modo que as
# inserções e remoções realizadas pelo cliente desta classe são sempre de folhas.
class InternalNode:
    def __init__(self, max_key, sum_weights, max_suffix, parent, left, right):
        self.max_key = max_key              # guarda a maior chave (instante de tempo) da subávore esquerda enraizada neste nó interno. Essa árvore sempre existe porque é um nó interno
        self.sum_weights = sum_weights      # soma dos pesos das folhas da árvore enraizada nesse nó interno (é o numero de pushs menos o número de pops)
        self.max_suffix = max_suffix        # maior soma de pesos (operações) dos sufixos do conjunto das folhas enraizadas neste nó
        self.parent = parent
        self.left = left
        self.right = right
        self.is_leaf = False

    def is_root(self):
        return self.parent is None

    def set_color(self, color):
        self.color = color

    def is_red(self):
        return self.color

    def is_black(self):
        return not self.color

class Leaf:
    def __init__(self, time, operation, value):
        self.time = time                     # tempo em que foi realizada a operação
        self.operation = operation           # +1 se temos um push e -1 se temos um pop
        self.value = value                   # Valor que foi inserido na pilha, quando temos um push, ou None, caso a operação seja um pop
        self.max_key = self.time             # Os atributos a seguir foram feitos para uniformidade de nome dos atributos dos nós, de modo a deixar o código com menos casos
        self.max_suffix = max(0, operation)
        self.sum_weights = self.operation
        self.is_leaf = True

    def is_root(self):
        return self.parent is None

    def is_red(self):
        return False

    def is_black(self):
        return True

class RedBlackBST:

    def __init__(self):
        self.root = None

    def insert(self, time, operation, value):
        # Essa inserção serve exclusivamente para inserção de operações, e portanto inserimos um nó como folha da árvore
        if self.root is None:
            self.root = Leaf(time, operation, value)
            self.root.parent = None
            return

        parent = None
        node = self.root
        while not node.is_leaf:
            parent = node
            if time < node.max_key:
                node = node.left
            else:
                node = node.right

        dummy_node = Leaf(time, operation, value) # nó a ser inserido
        if time < node.time: # new_node é o pai da folha que foi inserida
            new_node = InternalNode(time, operation + node.operation,
                                    max(0, node.operation, node.operation + operation),
                                    node.parent, dummy_node, node)
        else:
            new_node = InternalNode(node.time, operation + node.operation,
                                    max(0, operation, operation + node.operation),
                                    node.parent, node, dummy_node)
        new_node.set_color(RED)
        dummy_node.parent = new_node
        node.parent = new_node
        if parent is None:
            self.root = new_node
        elif parent.right is node:
            parent.right = new_node
        else:
            parent.left = new_node

        self.fix_up_attributes(new_node)
        self.red_black_insert_fix_up(new_node)

    def fix_up_attributes(self, new_node):
        # esse método serve para corrigir os atributos de ascendentes de folhas que foram
        # removidas ou inseridas.
        node = new_node
        while node is not None:
            node.max_key = max(node.left.max_key, node.max_key)
            node.sum_weights = node.left.sum_weights + node.right.sum_weights
            node.max_suffix = max(node.right.max_suffix,
                                  node.right.sum_weights + node.left.max_suffix)
            node = node.parent

    def red_black_insert_fix_up(self, new_node):
        # Este método serve para a manutenção das propriedades da árvore rubro negra,
        # o que permite a manutenção de seu balanceamento.
        node = new_node
        while node.parent is not None and node.parent.is_red():
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
                        node = node.parent
                        self.rotate_left(node)
                        parent = node.parent # as rotacoes mudam node.parent mas nao mudam parent
                        grandparent = node.parent.parent
                    parent.set_color(BLACK)
                    grandparent.set_color(RED)
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
                        node = node.parent
                        self.rotate_right(node)
                        parent = node.parent # rotate muda node.parent mas nao parent
                        grandparent = node.parent.parent
                    parent.set_color(BLACK)
                    grandparent.set_color(RED)
                    self.rotate_left(grandparent)
        self.root.set_color(BLACK)

    def print_leaves(self):
        self._print_leaves(self.root)

    def _print_leaves(self, node):
        if node.is_leaf:
            if node.operation > 0:
                print("t:", node.time, " push(", node.value, ") ", end='')
            else:
                print("t:", node.time, " pop() ")
        else:
            self._print_leaves(node.left)
            self._print_leaves(node.right)

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        x.right.parent = x
        x.sum_weights = x.left.sum_weights + x.right.sum_weights
        x.max_suffix = max(x.right.max_suffix, x.right.sum_weights + x.left.max_suffix)
        y.parent = x.parent
        if x.is_root():
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        y.sum_weights = y.left.sum_weights + y.right.sum_weights
        y.max_suffix = max(y.right.max_suffix, y.right.sum_weights + y.left.max_suffix)
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        x.left.parent = x
        x.sum_weights = x.left.sum_weights + x.right.sum_weights
        x.max_suffix = max(x.right.max_suffix, x.right.sum_weights + x.left.max_suffix)
        y.parent = x.parent
        if x.is_root():
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        y.sum_weights = y.left.sum_weights + y.right.sum_weights
        y.max_suffix = max(y.right.max_suffix, y.right.sum_weights + y.left.max_suffix)
        x.parent = y

    def search_leaf(self, node, time): # esse método supõe que existe alguma folha com time procurado
        if node.is_leaf:
            return node
        if time <= node.max_key:
            return self.search_leaf(node.left, time)
        else:
            return self.search_leaf(node.right, time)

    def delete(self, time): # esse método serve exclusivamente para folhas
        node = self.search_leaf(self.root, time)
        if node.is_root():
            self.root = None
            return
        self._delete(node)

    def _delete(self, node):
        internal_delete = node.parent
        if node is internal_delete.left:
            sibling = internal_delete.right
        else:
            sibling = internal_delete.left
        grandparent = internal_delete.parent

        sibling.parent = grandparent
        if grandparent is None:
            self.root = sibling
            return
        if internal_delete is grandparent.left:
            grandparent.left = sibling
        else:
            grandparent.right = sibling

        self.fix_up_attributes(grandparent)
        if internal_delete.is_black():
            self.red_black_delete_fix_up(sibling)

    def red_black_delete_fix_up(self, x):
        # Cabe aqui a seguinte observação: ao olhar para o código, poderíamos pensar que
        # talvez em algum momento ele não funcione pois w, poderia, em pricípio,
        # ser uma folha e este método tentaria acessar atributos que não w não possui.
        # Entretanto, quando este código for executado, temos certeza
        # de que essa situação não ocorrerá. Isso porque uma configuração em que
        # w seja uma folha violaria (antes da remoção!!) as propriedades da árvore rubro negra.
        # ^ não tenho tanta certeza assim de que isso não pode acontecer durante a execucao, mais para cima.
        # parece que não
        while x is not self.root and x.is_black():
            if x is x.parent.left:
                w = x.parent.right
                if w.is_red():
                    w.set_color(BLACK)
                    x.parent.set_color(RED)
                    self.rotate_left(x.parent)
                    w = x.parent.right
                if w.left.is_black() and w.right.is_black():
                    w.set_color(RED)
                    x = x.parent
                else:
                    if w.right.is_black():
                        w.left.set_color(BLACK)
                        w.set_color(RED)
                        self.rotate_right(w)
                        w = x.parent.right
                    w.set_color(x.parent.color)
                    x.parent.set_color(BLACK)
                    w.right.set_color(BLACK)
                    self.rotate_left(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.is_red():
                    w.set_color(BLACK)
                    x.parent.set_color(RED)
                    self.rotate_right(x.parent)
                    w = x.parent.left
                if w.left.is_black() and w.right.is_black():
                    w.set_color(RED)
                    x = x.parent
                else:
                    if w.left.is_black():
                        w.right.set_color(BLACK)
                        w.set_color(RED)
                        self.rotate_left(w)
                        w = x.parent.left
                    w.set_color(x.parent.color)
                    x.parent.set_color(BLACK)
                    w.left.set_color(BLACK)
                    self.rotate_right(x.parent)
                    x = self.root
        if not x.is_leaf:
            x.set_color(BLACK)

    def floor(self, time):
        #  dada uma chave time, que representa um instante, floor devolve o valor
        # da maior chave (time) menor ou igual a key
        floor_node = self._floor_node(self.root, time)
        if floor_node is None:
            return None
        return floor_node.time

    def _floor_node(self, node, time):
        if node.is_leaf:
            if time >= node.time:
                return node
            return None
        if time <= node.max_key:
            return self._floor_node(node.left, time)
        candidate = self._floor_node(node.right, time)
        if candidate is not None:
            return candidate
        return self._floor_node(node.left, time)

    def debug_red_black(self):
        # os métodos a seguir servem para checar a validade das propriedades das árvores rubro negra
        if self.root_is_red():
            print("Raiz vermelha!")
        if self.red_node_with_red_child():
            print("Há um nó vermelho com algum filho também vermelho!")
        if not self.black_height_unique():
            print("Há um nó com altura negra não bem definida")
        if self.red_leafs():
            print("Há uma folha vermelha")

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

    def red_leafs(self):
        return self._red_leafs(self.root)

    def _red_leafs(self, node):
        if node.is_leaf: # na verdade queremos saber se há nós da classe InternalNode vermelhos e sem filhos
            return False
        if node.is_red() and (node.left is None or node.right is None):
            return True
        return self._red_leafs(node.left) or self._red_leafs(node.right)

    def black_height_unique(self):
        return self._black_height_unique(self.root)

    def _black_height_unique(self, node):
        if node.is_leaf:
            return True
        leaves = self._find_leaves(node)
        black_height = self._number_black_nodes(node, leaves[0].time)
        for leaf in leaves[1:]:
            new_black_height = self._number_black_nodes(node, leaf.time)
            if new_black_height != black_height:
                return False
        return (self._black_height_unique(node.left)
                and self._black_height_unique(node.right))

    def _find_leaves(self, node):
        if node.is_leaf:
            return [node]
        return self._find_leaves(node.left) + self._find_leaves(node.right)

    def _number_black_nodes(self, node, leaf_key):
        if node.is_leaf:
            return 0
        if leaf_key <= node.max_key:
            black_nodes = self._number_black_nodes(node.left, leaf_key)
            if node.left.is_black():
                black_nodes += 1
        else:
            black_nodes = self._number_black_nodes(node.right, leaf_key)
            if node.right.is_black():
                black_nodes += 1
        return black_nodes

    def kth(self, time, k):
        # Primeiro encontramos o nó cuja variável de instância
        # time é a maior possível e é menor que  o time fornecido a kth
        node_time = self._floor_node(self.root, time)
        # no resto da execução, k representa o k-ésimo push da direita para
        # a esquerda a partir da folha node_time
        k -= node_time.operation 
        if k == 0: # se k for zero, estamos buscando o nó em que estamos
            return node_time.value

        # Se k não for zero, então devemos buscar o k-ésimo push da direita para a esquerda de node_time.
        # Para tanto, precisamos subir na árvore até que encontremos
        # o primeiro nó que é ascendente desse push no percurso de node_time até a raiz.
        # current_node representará os candidatos a esse nó nesse percurso.
        # Depois de cada execução de next_stop, current_node apontará para o 
        # primeiro nó que é pai de folhas passadas a node_time que ainda não
        # foram levadas em consideração. Mais detalhes sobre next_stop estão em sua 
        # implementação
        previous_node = node_time
        current_node = node_time.parent
        current_node, previous_node = RedBlackBST.next_stop(current_node,
                                                            previous_node)
        go_up = True
        while go_up:
            if current_node.left.max_suffix < k:
                # se a quantidade máxima de novos (novos no sentido de que não foram examinados)
                # pushs não anulados por pops (= current_node.left.max_suffix)
                # não for pelo menos igual a k, então precisamos buscar mais
                # pushs. Entretanto, precisamos "descontar" (pode na realidade aumentar) a quantidade de
                # pushs que já encontrados. Teremos que buscar folhas mais à esquerda
                k -= current_node.left.sum_weights
                previous_node = current_node
                current_node = current_node.parent
                current_node, previous_node = RedBlackBST.next_stop(current_node,
                                                                    previous_node)
            else:
                go_up = False

        # Neste momento, sabemos que current node é 
        # o primeiro nó no percurso da folha node_time até a raiz 
        # que é ascendente do push que inseriu
        # o elemento procurado. Assim, devemos descer na árvore enraizada nele
        current_node = current_node.left
        while not current_node.is_leaf:
            # devemos decidir se a folha que contem o elemento procurado
            # está à direita ou à esquerda de current_node.
            if current_node.right.max_suffix >= k:
                # se a quantidade máxima de pushs não anulados por pops à direita for pelo menos
                # igual a k, então sabemos que kth está a direita e k continua sendo
                # o k-ésimo push mais à direita
                current_node = current_node.right
            else:
                # se não, o nó procurado está à esquerda, mas devemos 
                # descontar os pushs que "já vimos" à direita, o que é 
                # feito na linha abaixo
                k -= current_node.right.sum_weights
                current_node = current_node.left

        return current_node.value

    def top(self, time):
        return self.kth(time, 1)

    def find_leaves_up_to(self, time):
        time = self.floor(time)
        return self._find_leaves_up_to(self.root, time)

    def _find_leaves_up_to(self, node, time):
        if node.is_leaf:
            if node.time <= time:
                return [node]
            return []
        if node.max_key <= time:
            return (self._find_leaves_up_to(node.left, time)
                    + self._find_leaves_up_to(node.right, time))
        return self._find_leaves_up_to(node.left, time)

    @staticmethod
    def next_stop(current_node, previous_node):
        # Vamos chamar de previous0 valor de previous_node no momento 
        # da chamada desta função. O valor de current_node ao fim da
        # execução dessa função deve ser o primeiro nó no caminho 
        # entre previous0 e a raiz da árvore tal que a árvore enraizada 
        # current_node.left contém folhas que ainda não foram levadas em consideração
        # na busca de kth. Em particular, essas folhas folhas devem ter time 
        # menores que as folhas da árvore enraizada em previous0.
        # Por isso, subimos na árvore até que previous_node aponte
        # para um nó que é filho direito de current_node;
        # dessa forma temos certeza de que a árvore enraizada em current_node.left
        # contem folha mais velhas que as folhas da árvore enraizada em previous0
        while current_node is not None and previous_node is current_node.left:
            previous_node = current_node
            current_node = current_node.parent
        return current_node, previous_node

    def weight_up_to(self, time):
        time = self.floor(time)
        return self._weight_up_to(time)

    def _weight_up_to(self, time):
        # devolve a soma dos pesos das folhas cujas variáveis de instância
        # time são menores ou iguais ao parâmetro time, dessa função
        weight = 0
        node = self.root
        while not node.is_leaf:
            if node.max_key < time:
                weight += node.left.sum_weights
                node = node.right
            else:
                node = node.left
        weight += node.sum_weights
        return weight
