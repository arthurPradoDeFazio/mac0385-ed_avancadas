import Substring as sub
import HashTable as ht

class VS:
    def __init__(self, string):
        """Objeto Vetor de Sufixos de uma string. Em primeiro, acrescentamos o caracter $
        à string em questão, o vetor de sufixos é uma lista com objetos do tipo Suffix, 
        implementados no arquivo Substring. Ao invés de utilizar os vetores LCP, LLCP, e RLCP,
        conform sugerido em aula, utilizei uma tabela de símbolos self.lcp_table cujas chaves são
        os pares (não é bem isso) L e R que podem ocorrer na execução de uma busca 
        binária e os valores associados a essa chave são lcp(L, R). Optei por 
        fazer dessa forma porque estava com dificuldade de me de que um valor de M na busca binária identifica um
        segmento L, R e porque achei que ficaria com o código mais simples; a ideia veio depois de consultar o livro 
        de Dan Gusfield, recomendado para essa tarefa e observar a figura 7.7 e pensar que bastam os pares L, R.
        
        Na verdade, as chaves armazenadas não são os pares LR propriamente ditos, e sim o número
        h = L * len(self.suffix_array) + R, mas esse número identifica o par L, R pois
        L = h // len(self.suffix_array e R = h % len(self.suffix_array), que nem fizemos nas florestas dinâmicas."""
        self.string = "".join([string, "$"])
        self.suffix_array = [sub.Suffix(self.string, i) for i in range(0, len(self.string))]
        self.suffix_array.sort()
        self.lcp_table = ht.HashTable()
        self.make_lcp()

    @staticmethod
    def lcp_len(s, t):
        """Calcula o comprimento do prefixo comum mais longo entre duas strings s e t
        
        Aqui ele é utilizado para calcular o comprimento do lcp entre dois 
        sufixos consecutivos no array de sufixos
        """
        i = 0
        while i < len(s) and i < len(t) and s[i] == t[i]:
            i += 1
        return i

    def lcp(self, i, j=-1):
        """ Devolve o lcp entre i e j, para os pares de i e j que podem ocorrer
        numa busca binária.

        Se nenhum valor for dado a j, devolve-se lcp(i - 1, i). Esse método 
        supõe que o lcp requisitado já tenha sido calculado.
        """
        if j == -1:
            j = i - 1
        if j < i:
            i, j = j, i
        return self.lcp_table.get(i * len(self.string) + j).value

    def make_lcp(self):
        """ Preenche a tabela de hash self.lcp_table para que as queries 
        self.lcp(i, j) possam ser respondidas em tempo constante. É importante 
        notar que nem todos os valores de i e j serão associados a um valor de 
        lcp, apenas aqueles tais que i e j são valores de dois extremos de um 
        segmento no vetor de sufixos de self.string quando se executa uma busca
        binária sobre ele.
        """
        self._make_lcp(0, len(self.string) - 1)

    def _make_lcp(self, l, r):
        """ Esse método de fato preenche a tabela de hash self.lcp_table 
        conforme explicado acima.

        Esse preenchimento é feito conforme o algoritmo explicado em aula.
        Os pares (chave, valor) armazenados na tabela de hash são tais que,
        valor é o lcp associado ao par de valores (que são os índices de dois
        sufixos de self.string) que está "codificado" pela chave. Se l e r 
        denotam os índices de dois sufixos, então a chave associada a esse par
        é l * |T| + r, em que |T| é o comprimento de self.string.
        """
        if r == l + 1:
            lr_lcp_len = VS.lcp_len(self.suffix_array[l], self.suffix_array[r])
        else:
            m = (l + r) // 2
            self._make_lcp(l, m)
            self._make_lcp(m, r)
            lr_lcp_len = min(self.lcp(l, m), self.lcp(m, r))

        self.lcp_table.put(ht.HashNode(l * len(self.string) + r, lr_lcp_len))

    def first_ocurrence(self, p):
        """ Se p é maior que todos os sufixos do texto, first_ocurrence devolve
        uma tupla com o comprimento do vetor de sufixos. Senão, first_ocurrence
        devolve uma tupla (R, r), em que R é a posição no vetor de sufixos do menor
        sufixo (contando com o caracter "$") que é maior que p e r é o número de 
        caracteres entre esse sufixo e p. 
        
        Note que se p ocorre no texto, então R é a primeira posição no vetor de sufixos 
        tal que o sufixo nessa posição contem p como prefixo. 
        
        Com efeito, o invariante mantido ao longo do while principal é 
        self.suffix_array[L] < p < self.suffix_array[R]. Assim, quando L == R - 1,
        e temos que p ocorre no texto, self.suffix_array[L] não poderia conter p, pois
        se assim o fosse, p seria um prefixo desse sufixo, de modo que o invariante estaria violado.
        Por outro lado, se p não fosse prefixo de self.suffix_array[R] então não haveria 
        ocorrência alguma de p no texto visto que as ocorrências de p devem estar entre 
        self.suffix_array[L] e self.suffix_array[R].

        Para um cliente desse método, o fato de que p ocorre no texto é
        garantido se r == len(p), conforme utiliza-se em search.

        O algoritmo utilizado é que foi apresentado em aula para busca da 
        primeira ocorrência, com algumas modificações que justifiquei nos 
        parágrafos acima.
        """
        r = VS.lcp_len(self.suffix_array[-1], p)
        if r < len(p) and p[r] > self.suffix_array[-1][r]:
            return len(self.suffix_array) - 1, r

        l = 0
        L = 0
        R = len(self.suffix_array) - 1
        while L < R - 1:
            M = (L + R) // 2
            if l == r:
                # compara p e M a partir de l + 1
                i = l
                while i < len(p) and p[i] == self.suffix_array[M][i]: # me parece que a condição i < len(self.suffix_array[M]) é dispensável por conta do $ que há em seu final
                    i += 1

                if i == len(p) or p[i] < self.suffix_array[M][i]:
                    R = M
                    r = i
                else:
                    L = M
                    l = i
            elif l > r:
                if l < self.lcp(L, M):
                    L = M
                elif self.lcp(L, M) < l:
                    R = M
                    r = self.lcp(L, M)
                else:
                    # compara p e M a  partir de l + 1
                    i = l
                    while i < len(p) and p[i] == self.suffix_array[M][i]:
                        i += 1

                    if i == len(p) or p[i] < self.suffix_array[M][i]:
                        R = M
                        r = i
                    else:
                        L = M
                        l = i
            else:
                if r < self.lcp(M, R):
                    R = M
                elif self.lcp(M, R) < r:
                    L = M
                    l = self.lcp(R, M)
                else:
                    # compara p e M a partir de r + 1
                    i = r
                    while i < len(p) and p[i] == self.suffix_array[M][i]:
                        i += 1

                    if i == len(p) or p[i] < self.suffix_array[M][i]:
                        R = M
                        r = i
                    else:
                        L = M
                        l = i
        return R, r

    def last_ocurrence(self, p):
        """Podemos supor que last_ocurrence será utilizado apenas se soubermos 
        que já há alguma ocorrência de p no texto. Neste, caso, last_ocurrence
        devolve um tupla (I, i), em que I é a posição no vetor de sufixos do último
        sufixo (em ordem lexicográfica) que possui p como prefixo, i é o 
        comprimento do maior prefixo comum entre p e self.suffix_array[I].

        Note que o algoritmo utilizado é essencialmente o mesmo de 
        first_ocurrence, com algumas modificações: em primeiro acrescentamos 
        o caracter "~" ao fim de p, e depois, devolvemos (L, l), ao invés de
        (R, r), como foi feito em first_ocurrence. Aqui, supus que ~ não ocorre no texto,
        nem na palavra e é o maior caracter do alfabeto com que estamos trabalhando.

        Aqui a justificativa: novamente o invariante do loop principal é que 
        self.suffix_array[L] < p~ < self.suffix_array[R] e supomos que p ocorre no texto. Agora examinamos o 
        momento em que R = L + 1. Note que p não pode ser prefixo de self.suffix_array[R] pois isso
        faria com que p~ fosse maior que self.suffix_array[R], já que certamente há mais um caracter além
        do último caracter de p em self.suffix_array[R]. Por outro lado, self.suffix_array[L] certamente
        tem p como prefixo já que se ocorresse mismatch antes do fim de p, não haveria nenhuma ocorrência de p
        no texto.        
        """
        r = VS.lcp_len(self.suffix_array[-1], p)
        if r == len(p):
            return len(self.suffix_array) - 1, r

        p = "".join([p, "~"]) # estou supondo que "~" é um caracter que não ocorre no texto e é o maior caracter do alfabeto

        l = 0
        L = 0
        R = len(self.suffix_array) - 1
        while L < R - 1:
            M = (L + R) // 2
            if l == r:
                # compara p e M a partir de l + 1
                i = l
                while i < len(p) and p[i] == self.suffix_array[M][i]: # me parece que a condição i < len(self.suffix_array[M]) é dispensável por conta do $ que há em seu final
                    i += 1

                if i == len(p) or p[i] < self.suffix_array[M][i]:
                    R = M
                    r = i
                else:
                    L = M
                    l = i
            elif l > r:
                if l < self.lcp(L, M):
                    L = M
                elif self.lcp(L, M) < l:
                    R = M
                    r = self.lcp(L, M)
                else:
                    # compara p e M a  partir de l + 1
                    i = l
                    while i < len(p) and p[i] == self.suffix_array[M][i]:
                        i += 1

                    if i == len(p) or p[i] < self.suffix_array[M][i]:
                        R = M
                        r = i
                    else:
                        L = M
                        l = i
            else:
                if r < self.lcp(M, R):
                    R = M
                elif self.lcp(M, R) < r:
                    L = M
                    l = self.lcp(R, M)
                else:
                    # compara p e M a partir de r + 1
                    i = r
                    while i < len(p) and p[i] == self.suffix_array[M][i]:
                        i += 1

                    if i == len(p) or p[i] < self.suffix_array[M][i]:
                        R = M
                        r = i
                    else:
                        L = M
                        l = i
        return L, l

    def search(self, p):
        """Devolve True se p ocorre no texto e False caso contrário."""
        return self.first_ocurrence(p)[1] == len(p)

    def ocurrences(self, p):
        """Devolve uma lista com os índices no texto dos sufixos que contem
        p com prefixo. """
        ocurrences = []
        first_ocurrence = self.first_ocurrence(p)
        if first_ocurrence[1] < len(p):
            return ocurrences

        last_ocurrence = self.last_ocurrence(p)
        return [suffix.first_char_index for suffix in self.suffix_array[first_ocurrence[0]:last_ocurrence[0] + 1]]

    def nocurrences(self, p):
        """Devolve o número de ocorrências de p no texto."""
        first_ocurrence = self.first_ocurrence(p)
        if first_ocurrence[1] < len(p):
            return 0
        return self.last_ocurrence(p)[0] - first_ocurrence[0] + 1

    def print(self):
        print("Vetor de sufixos")
        for suffix in self.suffix_array:
            print(suffix)
        print("Vetor LCP:")
        for i in range(1, len(self.suffix_array)):
            print(self.lcp(i))


    ################ Debug functions #######################################
    def debug(self):
        if self.incorrect_sort():
            print("Vetor de sufixos ordenado incorretamente")
        if self.wrong_lcp():
            print("LCP errado")

    def incorrect_sort(self):
        for i in range(0, len(self.suffix_array) - 1):
            if self.suffix_array[i] > self.suffix_array[i + 1]:
                return True
        return False
    
    def wrong_lcp(self):
        for node in self.lcp_table.table:
            if node is not None:
                l = node.key // len(self.suffix_array)
                r = node.key % len(self.suffix_array)
                if node.value != VS.lcp_len(self.suffix_array[l], self.suffix_array[r]):
                    return True
        return False

    def print_vs(self):
        for suffix, i in zip(self.suffix_array, range(len(self.suffix_array))):
            print(i, suffix)