class LinkedListNode:
    def __init__(self, item, next):
        self.item = item
        self.next = next

class LinkedList:
    def __init__(self):
        self.first = None
        self.last = None
        self.length = 0

    def __iter__(self):
        current_node = self.first
        while current_node is not None:
            yield current_node.item
            current_node = current_node.next

    def __len__(self):
        return self.length

    def __str__(self):
        r = ""
        for i in self:
            r += str(i) + " "
        return r

    def append(self, item):
        self.first = LinkedListNode(item, self.first)
        if self.last is None:
            self.last = self.first
        self.length += 1

    def merge(self, other):
        if self.is_empty():
            self.first = other.first
            self.last = other.last
            self.length = other.length
            return
        if other.is_empty():
            return

        self.last.next = other.first
        self.last = other.last
        self.length += other.length

    def is_empty(self):
        return self.length == 0
