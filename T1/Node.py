# Arthur Prado De Fazio
# NUSP: 9298614
# Esta implementação foi fortemente baseada no pseudo-código disponível
# na tese de mestrado de Yan Couto

class Node:
    def __init__(self, parent=None, depth=0, val=None):
        self.parent = parent
        self.depth = depth
        self.val = val
        if depth == 0: # é raiz
            self.jump = self
        else:
            self.add_leaf()

    def add_leaf(self):
        parent = self.parent
        if parent.jump.depth != 0 and parent.depth - parent.jump.depth == parent.jump.depth - parent.jump.jump.depth:
            self.jump = parent.jump.jump
        else:
            self.jump = parent

    def level_ancestor(self, ancestor):
        ancestor_depth = self.depth - ancestor
        while self.depth != ancestor_depth:
            if self.jump.depth >= ancestor_depth:
                self = self.jump
            else:
                self = self.parent
        return self

    def lowest_common_ancestor(self, relative):
        if self.depth > relative.depth:
            self, relative = relative, self
        relative = relative.level_ancestor(relative.depth - self.depth)
        if self is relative:
            return self
        while self.parent is not relative.parent:
            if self.jump is not relative.jump:
                self = self.jump
                relative = relative.jump
            else:
                self = self.parent
                relative = relative.parent
        return self.parent
