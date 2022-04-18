import math

RED = True
BLACK = False

class OperationLeaf:
    # essa classe modela um nó que guarda uma operação feita sobre o heap
    # esses nós são folhas de uma árvore da classe OperationRedBlackBST
    def __init__(self, time, weight, value):
        self.time = time # tempo em que ocorre a operação
        self.weight = weight # operação: 1 se for insert q nao esta no qnow, 0, se esta, -1 se for deletemin
        self.value = value # valor inserido ou None se for um deletemin
        self.max_time_left = time # maior tempo à esquerda
        self.sum_weights = weight # soma dos pesos
        self.operation = weight #operação, no caso das folhas, weight = operation
        self.max_suffix_sum = max(0, weight) # soma mínima de sufixo da árvore enraizada neste nó
        self.min_prefix_sum = min(0, weight)
        if weight == 1:
            self.max_one_node = self
            self.min_zero_node = None
        elif weight == 0:
            self.max_one_node = None
            self.min_zero_node = self
        else:
            self.max_one_node = None
            self.min_zero_node = None
        self.is_leaf = True

    def is_red(self):
        return False

    def is_black(self):
        return True

    def change_weight(self, new_weight): # supumos aqui que mudanças de peso só ocorrem de 0 para 1 ou 1 para 0
        self.weight = new_weight
        self.sum_weights = new_weight
        self.operation = new_weight
        self.max_suffix_sum = max(0, new_weight)
        self.min_prefix_sum = min(0, new_weight)
        if new_weight == 1:
            self.max_one_node = self
            self.min_zero_node = None
        elif new_weight == 0:
            self.max_one_node = None
            self.min_zero_node = self

class InternalOperationNode:
    # Essa classe representa os nós internos de uma árvore de operações de um heap
    # Esses são os nós internos de uma árvore da classe OperationRedBlackBST
    def __init__(self, parent, left, right):
        self.max_time_left = left.time # o maior tempo das folhas na subárvore esquerda da árvore enraizada neste nó
        self.sum_weights = left.sum_weights + right.sum_weights # soma dos pesos das folhas da árvore enraizada neste nó
        self.max_suffix_sum = max(right.max_suffix_sum, left.max_suffix_sum + right.sum_weights) # maior soma de todos os sufixos do conjunto de folhas da árvore enraizada neste nó
        self.min_prefix_sum = min(left.min_prefix_sum, left.sum_weights + right.min_prefix_sum) # menor soma de todos os prefixos do conjunto de folhas da árvore enraizada neste nó
        self.max_one_node = InternalOperationNode._max_one_node(left, right) # referência para a folha de peso 1 com maior value
        self.min_zero_node = InternalOperationNode._min_zero_node(left, right) # referência para a folha de peso 0 com menor value
        self.parent = parent
        self.left = left
        self.right = right
        self.is_leaf = False

    def update_attributes(self):
        # Atualização dos atributos de um nó interno quand ocorre alguma 
        # mudança em seus filhos, seja essa mudança nos atributos, seja
        # nos ponteiros left ou right de left.
        self.sum_weights = self.left.sum_weights + self.right.sum_weights
        self.max_suffix_sum = max(self.right.max_suffix_sum, self.left.max_suffix_sum + self.right.sum_weights)
        self.min_prefix_sum = min(self.left.min_prefix_sum, self.left.sum_weights + self.right.min_prefix_sum)
        self.max_one_node = InternalOperationNode._max_one_node(self.left, self.right)
        self.min_zero_node = InternalOperationNode._min_zero_node(self.left, self.right)

    @staticmethod
    def _max_one_node(left, right):
        # dado um nó cujas subárvores esquerda e direita estão enraizadas em 
        # left e right, respectivamente, _max_one_node devolve uma referência 
        # para a folha de peso 1 com maior value que é descendente desse nó
        if left.max_one_node is None:
            return right.max_one_node
        if right.max_one_node is None:
            return left.max_one_node
        if left.max_one_node.value < right.max_one_node.value:
            return right.max_one_node
        return left.max_one_node

    @staticmethod
    def _min_zero_node(left, right):
        # Análogo ao método acima
        if left.min_zero_node is None:
            return right.min_zero_node
        if right.min_zero_node is None:
            return left.min_zero_node
        if left.min_zero_node.value < right.min_zero_node.value:
            return left.min_zero_node
        return right.min_zero_node

    def set_color(self, color):
        self.color = color

    def is_red(self):
        return self.color

    def is_black(self):
        return not self.color

class OperationRedBlackBST:
    # Essa classe guarda uma árvore rubro negra cujas folhas representam as 
    # operações feitas sobre um heap. As folhas estão ordenadas pelo instante
    # em que a operação foi feita, armazenada no atributo time dos objetos de 
    # OperationLeaf
    def __init__(self):
        self.root = None

    #################### Métodos típicos de uma árvore rubro negra ##########################################

    def _search_leaf(self, time): # esse método supõe que existe folha com atributo time igual a time
        node = self.root
        while not node.is_leaf:
            if time <= node.max_time_left:
                node = node.left
            else:
                node = node.right
        return node

    def floor_leaf(self, time):
        # devolve a maior folha com atributo time menor ou igual a time
        if self.root is None:
            return None
        return self._floor_leaf(self.root, time)

    def _floor_leaf(self, node, time):
        if node.is_leaf:
            if time < node.time:
                return None
            return node
        if time <= node.max_time_left:
            return self._floor_leaf(node.left, time)
        candidate = self._floor_leaf(node.right, time)
        if candidate is not None:
            return candidate
        return self._floor_leaf(node.left, time)

    def ceiling_leaf(self, time):
        # devolve a menor folha com atributo time maior ou igual a time
        if self.root is None:
            return None
        return self._ceiling_leaf(self.root, time)

    def _ceiling_leaf(self, node, time):
        if node.is_leaf:
            if time > node.time:
                return None
            return node
        if time > node.max_time_left:
            return self._ceiling_leaf(node.right, time)
        return self._ceiling_leaf(node.left, time)

    def max_node(self, node):
        while not node.is_leaf:
            node = node.right
        return node



    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        x.right.parent = x
        y.parent = x.parent

        x.update_attributes()

        if x is self.root:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        x.parent = y
        y.left = x

        y.update_attributes()

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        x.left.parent = x
        y.parent = x.parent

        x.update_attributes()

        if x is self.root:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        x.parent = y
        y.right = x

        y.update_attributes()

    def fix_up_attributes(self, node):
        # Corrige os atributos de uma árvore após a inserção de uma folha
        while node is not None:
            node.update_attributes()
            node = node.parent

    def fix_max_up(self, node):
        # Esse método corrige o atributo max_time_left de um único nó.
        # Esse método é utilizando apenas quando ocorre a remoção de uma folha, e
        # foi feito para corrigir o atributo max_time_left do nó que possuía o tempo 
        # da folha removida com max_time_left
        n = node
        while n.parent is not None and n is not n.parent.left:
            n = n.parent
        if n.parent is not None:
            while not node.is_leaf:
                node = node.right
            n.parent.max_time_left = node.time



    def insert(self, time, operation, value):
        # Insere uma folha com atributos time, operation e value na árvore, 
        # acrescentando um nó interno e fazendo as alterações necessárias
        # nos nós internos para que guardem os atributos corretos
        if self.root is None:
            self.root = OperationLeaf(time, operation, value)
            self.root.parent = None
            return

        parent = None
        current_node = self.root
        while not current_node.is_leaf:
            parent = current_node
            if time < current_node.max_time_left:
                current_node = current_node.left
            else:
                current_node = current_node.right

        dummy_node = OperationLeaf(time, operation, value)
        if time < current_node.time:
            new_node = InternalOperationNode(parent, dummy_node, current_node)
        else:
            new_node = InternalOperationNode(parent, current_node, dummy_node)
        new_node.set_color(RED)
        dummy_node.parent = new_node
        current_node.parent = new_node
        if parent is None:
            self.root = new_node
        elif parent.left is current_node:
            parent.left = new_node
        else:
            parent.right = new_node

        self.fix_up_attributes(new_node)
        self.red_black_insert_fix_up(new_node)

    def red_black_insert_fix_up(self, node):
        # esse método realiza a manutenção do balanceamento de uma árvore
        # rubro negra após a inserção de uma folha
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
                        node = parent
                        self.rotate_left(node)
                        parent = node.parent
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
                        node = parent
                        self.rotate_right(node)
                        parent = node.parent
                        grandparent = node.parent.parent

                    grandparent.set_color(RED)
                    parent.set_color(BLACK)
                    self.rotate_left(grandparent)

        self.root.set_color(BLACK)

    def delete(self, time):
        # Remove a folha com atributo time, fazendo as correções necessárias
        # nos nós internos
        leaf_to_delete = self._search_leaf(time)

        if leaf_to_delete is self.root:
            self.root = None
            return

        internal_node_to_delete = leaf_to_delete.parent
        grandparent = leaf_to_delete.parent.parent
        if leaf_to_delete is internal_node_to_delete.left:
            sibling = internal_node_to_delete.right
        else:
            sibling = internal_node_to_delete.left

        sibling.parent = grandparent
        if grandparent is None:
            self.root = sibling
            if sibling.is_red():
                sibling.set_color(BLACK)
            return
        if internal_node_to_delete is grandparent.left:
            grandparent.left = sibling
        else:
            grandparent.right = sibling

        if leaf_to_delete is internal_node_to_delete.right:
            self.fix_max_up(sibling)
        self.fix_up_attributes(grandparent)
        if internal_node_to_delete.is_black():
            self.red_black_delete_fix_up(sibling)

    def red_black_delete_fix_up(self, node):
        # Corrige o balanceamento da árvore rubro negra após a remoção
        # de uma folha
        while node is not self.root and node.is_black():
            parent = node.parent
            if node is parent.left:
                sibling = parent.right
                if sibling.is_red():
                    sibling.set_color(BLACK)
                    parent.set_color(RED)
                    self.rotate_left(parent)
                    sibling = parent.right

                if sibling.left.is_black() and sibling.right.is_black():
                    sibling.set_color(RED)
                    node = parent
                else:
                    if sibling.right.is_black():
                        sibling.left.set_color(BLACK)
                        sibling.set_color(RED)
                        self.rotate_right(sibling)
                        sibling = parent.right

                    sibling.set_color(parent.color)
                    parent.set_color(BLACK)
                    sibling.right.set_color(BLACK)
                    self.rotate_left(parent)
                    node = self.root
            else:
                sibling = parent.left
                if sibling.is_red():
                    sibling.set_color(BLACK)
                    parent.set_color(RED)
                    self.rotate_right(parent)
                    sibling = parent.left

                if sibling.left.is_black() and sibling.right.is_black():
                    sibling.set_color(RED)
                    node = parent
                else:
                    if sibling.left.is_black():
                        sibling.right.set_color(BLACK)
                        sibling.set_color(RED)
                        self.rotate_left(sibling)
                        sibling = parent.left

                    sibling.set_color(parent.color)
                    parent.set_color(BLACK)
                    sibling.left.set_color(BLACK)
                    self.rotate_right(parent)
                    node = self.root

        if not node.is_leaf:
            node.set_color(BLACK)

    
    ###############################################################################################################

    ####################### Métodos relacionados ao heap parcialmente retroativo ###################################

    def prefix_sum_up_to(self, leaf):
        # Dada uma referência para uma folha, prefix_sum_up_to devolve a soma
        # dos pesos de todas as folhas que têm time menor ou igual a leaf.time
        prefix_sum_up_to_leaf = 0
        current_node = self.root
        while current_node is not leaf:
            if leaf.time <= current_node.max_time_left:
                current_node = current_node.left
            else:
                prefix_sum_up_to_leaf += current_node.left.sum_weights
                current_node = current_node.right
        prefix_sum_up_to_leaf += leaf.weight
        return prefix_sum_up_to_leaf

    @staticmethod
    def next_stop_left(current_node, previous_node):
        # Considere o percurso que vai desde previous_node até a raiz
        # da árvore. Levando em conta que current_node é pai de previous_node,
        # next_stop_left, devolve dois nós de maneira que current_node é pai de 
        # previous_node e ambos pertencem ao percurso mencionado. Mais ainda,
        # current_node é o primeiro nó nesse percurso cujas folhas à esquerda
        # são mais antigas que as folhas da árvore enraizada em current_node
        while current_node is not None and previous_node is current_node.left:
            previous_node = current_node
            current_node = current_node.parent
        if current_node is None:
            return previous_node, previous_node
        return current_node, previous_node

    @staticmethod
    def next_stop_right(current_node, previous_node):
        # Análogo ao método acima, porém as folhas à direita de current_node 
        # são todas mais novas que as folhas da árvore enraizada em 
        # previous_node
        while current_node is not None and previous_node is current_node.right:
            previous_node = current_node
            current_node = current_node.parent
        if current_node is None:
            return previous_node, previous_node
        return current_node, previous_node

    def find_last_bridge(self, time):
        # Encontra a maior folha de tempor menor ou igual a time cuja soma
        # dos pesos até ela é 0. Ou seja, encontra a última ponte antes de time
        # ou até time
        floor_leaf = self.floor_leaf(time)
        if floor_leaf is None:
            return None

        prefix_sum_up_to_floor_leaf = self.prefix_sum_up_to(floor_leaf)

        if prefix_sum_up_to_floor_leaf == 0:
            return floor_leaf

        # Considere o caminho existente entre floor_leaf e a raiz da árvore,
        # percorrido nesse sentido. O trecho de código compreendido entre as 
        # linhas 429 e 443 tem o objetivo de encontrar o primeiro nó neste 
        # percurso que é ascendente da folha que representa a ponte mais recente
        # anterior a floor_leaf. Ao fim do while entre as linhas 435 e 443, 
        # ignorando a linha 438, current_node aponta para o nó desejado.
        k = prefix_sum_up_to_floor_leaf
        previous_node = floor_leaf
        current_node = floor_leaf.parent
        current_node, previous_node = OperationRedBlackBST.next_stop_left(current_node, previous_node)
        k -= floor_leaf.operation # a partir desse ponto, k sempre guarda a soma dos pesos das folhas quem tem time menor ou igual à folha com maior time na árvore current_node.left
        go_up = True
        while go_up:
            if current_node is self.root or k - current_node.left.max_suffix_sum <= 0: # vemos se, ao "abandonar" o sufixo de maior soma chegamos a peso zero, o que indica uma ponte, se sim, devemos descer
                go_up = False
                current_node = current_node.left
            else: # se não, abandonar apenas as folhas enraizadas em current_node.left não é suficiente para anular k, por isso subimos
                k -= current_node.left.sum_weights
                previous_node = current_node
                current_node = current_node.parent
                current_node, previous_node = OperationRedBlackBST.next_stop_left(current_node, previous_node)


        # O próximo while tem por objetivo chegar à folha mais à direita possível que é ponte
        while not current_node.is_leaf: # k armazena a soma dos pesos do prefixo definido pela folha de maior time em current.node.right
            if k - current_node.right.max_suffix_sum <= 0: # se abandonando o maior peso à direita, ficamos com k = 0, então o momento em que k = 0, deve estar à direita
                current_node = current_node.right
            else: # se não abanamos toda a subárvore direita e vamos para a esquerda
                k -= current_node.right.sum_weights
                current_node = current_node.left

        # podia ser mais elegante
        if current_node.weight == 1: # pode ser que cheguemos a um nó de peso 1 ao fim do while acima. Essa folha certamente não é uma ponte, então vamos para a folha anterior
            previous_node = current_node
            current_node = current_node.parent
            current_node, previous_node = OperationRedBlackBST.next_stop_left(current_node, previous_node)
            current_node = self.max_node(current_node.left)

        return current_node

    def find_next_bridge(self, time):
        # Encontra a folha que representa ponte mais à esquerda que está à direita de time
        # Esse método é análogo ao método acima
        ceiling_leaf = self.ceiling_leaf(time)
        if ceiling_leaf is None:
            return None

        prefix_sum_up_to_ceiling_leaf = self.prefix_sum_up_to(ceiling_leaf)

        if prefix_sum_up_to_ceiling_leaf == 0:
            return ceiling_leaf

        k = prefix_sum_up_to_ceiling_leaf
        previous_node = ceiling_leaf
        current_node = ceiling_leaf.parent
        current_node, previous_node = OperationRedBlackBST.next_stop_right(current_node, previous_node)
        go_up = True
        while go_up:
            if current_node is self.root or k + current_node.right.min_prefix_sum <= 0:
                go_up = False
                current_node = current_node.right
            else:
                k += current_node.right.sum_weights
                previous_node = current_node
                current_node = current_node.parent
                current_node, previous_node = OperationRedBlackBST.next_stop_right(current_node, previous_node)

        while not current_node.is_leaf:
            if k + current_node.left.min_prefix_sum <= 0:
                current_node = current_node.left
            else:
                k += current_node.left.sum_weights
                current_node = current_node.right

        return current_node   

    def max_one_node_from(self, leaf):
        # Devolve uma referência para a folha de peso 1 com maior value que tem
        # time maior ou igual a leaf.time
        if leaf is None:
            return None

        max_one_node = leaf.max_one_node
        previous_node = leaf
        current_node = leaf.parent
        while current_node is not None:
            current_node, previous_node = OperationRedBlackBST.next_stop_right(current_node, previous_node)
            if (current_node.right.max_one_node is not None 
                and current_node.right.max_one_node.time > leaf.time):
                if max_one_node is None:
                    max_one_node = current_node.right.max_one_node
                elif (current_node.right.max_one_node is not None 
                      and max_one_node.value < current_node.right.max_one_node.value):
                    max_one_node = current_node.right.max_one_node
            previous_node = current_node
            current_node = current_node.parent
        return max_one_node

    def min_zero_node_before(self, leaf):
        # Devolve uma referência para a folha de peso 0 com menor value que tem
        # time menor ou igual a leaf.time
        if leaf is None:
            return None

        min_zero_node = None # a princípio, tinha colocado leaf.min_zero_node, mas isso dá errado
        previous_node = leaf
        current_node = leaf.parent
        while current_node is not None:
            current_node, previous_node = OperationRedBlackBST.next_stop_left(current_node, previous_node)
            if (current_node.left.min_zero_node is not None
                and current_node.left.min_zero_node.time < leaf.time):
                if min_zero_node is None:
                    min_zero_node = current_node.left.min_zero_node
                elif min_zero_node.value > current_node.left.min_zero_node.value:
                    min_zero_node = current_node.left.min_zero_node
            previous_node = current_node
            current_node = current_node.parent
        return min_zero_node

    # Os quatro métodos abaixo são aqueles que serão efetivamente utilizados pela interface Heap
    def insert_insertion(self, time, value):
        if self.root is None:
            self.insert(time, 0, value)
            return value

        bridge = self.find_last_bridge(time)
        max_one_node = self.max_one_node_from(bridge) # max{I_{>= t'} - Q_now}
        if max_one_node is None or value > max_one_node.value:
            self.insert(time, 0, value) # se o valor a ser inserido, for maior que max_one_node.value, value entra com peso 0
            return value
        else:
            max_one_node.change_weight(0) # senão, devemos mudar o peso de max_one_node para zero e inserir value com peso 1
            self.fix_up_attributes(max_one_node.parent)
            self.insert(time, 1, value)
            return max_one_node.value

    def delete_deletion(self, time):
        bridge = self.find_last_bridge(time)
        if bridge is not None and bridge.time == time: # se o próprio delete que queremos remover for uma ponte, devemos procurar a ponte anterior, vide linha 7 do arqvuivo teste2.py
            node, _ = OperationRedBlackBST.next_stop_left(bridge.parent, bridge)
            bridge = self.find_last_bridge(self.max_node(node.left).time)
        max_one_node = self.max_one_node_from(bridge) # max{I_{>= t'} - Q_now}
        max_one_node.change_weight(0)
        self.fix_up_attributes(max_one_node.parent)
        self.delete(time)
        return max_one_node.value

    def insert_deletion(self, time):
        bridge = self.find_next_bridge(time)
        min_zero_node = self.min_zero_node_before(bridge) # min{I_{<=t'} \cap Q_now}
        min_zero_node.change_weight(1) 
        self.fix_up_attributes(min_zero_node.parent)
        self.insert(time, -1, None)
        return min_zero_node.value

    def delete_insertion(self, time):
        time_leaf = self.floor_leaf(time)
        if time_leaf.weight == 0: # se time_leaf.value já está em Q_now, é ele que deve ser removido
            value = time_leaf.value
            self.delete(time)
            return value

        bridge = self.find_next_bridge(time)
        min_zero_node = self.min_zero_node_before(bridge)
        min_zero_node.change_weight(1)
        self.fix_up_attributes(min_zero_node.parent)
        self.delete(time)
        return min_zero_node.value

    ################################################################################################################


    ######################## Métodos para depuração ################################################################

    def debug_red_black(self):
        if self.red_root():
            print("Raiz vermelha")
        if self.red_node_with_red_child():
            print("Nó vermelho com algum filho vermelho")
        if not self.black_height_unique():
            print("Altura negra não bem definida")
        if self.red_leaves():
            print("Há folhas vermelhas")

    def red_root(self):
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

    def downward_black_paths_to_leaves(self):
        return self._downward_black_paths_to_leaves(self.root)

    def _downward_black_paths_to_leaves(self, node):
        if node.is_leaf:
            return [[]]
        left_downward_black_paths_to_leaves = self._downward_black_paths_to_leaves(node.left)
        if node.left.is_black():
            for path in left_downward_black_paths_to_leaves:
                path.append(node.left)
        right_downward_black_paths_to_leaves = self._downward_black_paths_to_leaves(node.right)
        if node.right.is_black():
            for path in right_downward_black_paths_to_leaves:
                path.append(node.right)
        return (left_downward_black_paths_to_leaves
               + right_downward_black_paths_to_leaves)

    def black_height_unique(self):
        black_paths_to_leaves = self.downward_black_paths_to_leaves()
        black_height = len(black_paths_to_leaves[0])
        for path in black_paths_to_leaves[1:]:
            if len(path) != black_height:
                return False
        return True

    def red_leaves(self):
        return self._red_leaves(self.root)

    def _red_leaves(self, node):
        if node.is_leaf:
            return False
        if node.is_red() and (node.left is None or node.right is None):
            return True
        return self._red_leaves(node.left) or self._red_leaves(node.right)

    def print(self):
        # a impressão de um nó tem formato chave : prioridade
        self.display()

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
        if node.is_leaf:
            line = '%s:%s:%s' % (node.time, node.weight, node.value) # muda
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Two children.
        left, n, p, x = self._display_aux(node.left)
        right, m, q, y = self._display_aux(node.right)
        if node.min_zero_node is None:
            s = "N"
        else:
            s = '%s' % (node.min_zero_node.time)
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

    ###################################################################################################################