class Substring:
    def __init__(self, string, first_char_index, last_char_index):
        """Essa classe é identificada por uma string (a string da qual é substring), o índice do primeiro caracter
        e o índice do último caracter dessa substring. Para os efeitos da T9, como lidaremos apenas com
        sufixos, bastaria identificar um sufixo (que foi implementado como subclasse de Substring)
        pelo índice de seu primeiro caracter. A rigor não é necessário ter o ponteiro para a string
        da qual o objeto é substring, entretanto, achei que fazer dessa forma deixava o código mais limpo, do que
        se guardasse apenas o índice de ínicio, além disso, o acréscimo de memória por esse decisão é O(1) em
        relação a decisão de armazenar o apenas o índice de início."""
        if isinstance(string, Substring):
            self.string = string.string
            self.first_char_index = string.first_char_index + first_char_index
            self.last_char_index = string.first_char_index + last_char_index
        else:
            self.string = string
            self.first_char_index = first_char_index
            self.last_char_index = last_char_index
        self.len = last_char_index - first_char_index + 1

    def __len__(self):
        return self.len

    def __str__(self):
        return self.string[self.first_char_index: self.last_char_index + 1]

    def __getitem__(self, i):
        return self.string[self.first_char_index + i]

    def __lt__(self, other):
        i = j = 0
        while i < self.len and j < other.len:
            if self[i] == other[j]:
                i += 1
                j += 1
            elif self[i] < other[j]:
                return True
            else:
                return False
        
        if j >= other.len:
            return False
        return True

    def __gt__(self, other):
        i = j = 0
        while i < self.len and j < other.len:
            if self[i] == other[j]:
                i += 1
                j += 1
            elif self[i] < other[j]:
                return False
            else:
                return True
        
        if i >= self.len:
            return False
        return True

    def __eq__(self, other):
        i = j = 0
        while i < self.len and j <= other.len:
            if self[i] == other[j]:
                i += 1
                j += 1
            else:
                return False

        if i >= self.len and j >= other.len:
            return True
        return False

    def __le__(self, other):
        i = j = 0
        while i < self.len and j < other.len:
            if self[i] == other[j]:
                i += 1
                j += 1
            elif self[i] < other[j]:
                return True
            else:
                return False
        
        if i >= self.len:
            return True
        return False

    def __ge__(self, other):
        i = j = 0
        while i < self.len and j < other.len:
            if self[i] == other[j]:
                i += 1
                j += 1
            elif self[i] < other[j]:
                return False
            else:
                return True
        
        if j >= other.len:
            return True
        return False

class Prefix(Substring):
    def __init__(self, string, last_char_index):
        Substring.__init__(self, string, 0, last_char_index)

class Suffix(Substring):
    def __init__(self, string, first_char_index):
        Substring.__init__(self, string, first_char_index, len(string) - 1)