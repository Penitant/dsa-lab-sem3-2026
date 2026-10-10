class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None


class LL:
    def __init__(self):
        self.Head = None

    def add_element(self, x):
        # insert at head
        node = Node(x)
        node.next = self.Head
        self.Head = node

    def append(self, x):
        # insert at tail
        node = Node(x)
        if self.Head is None:
            self.Head = node
            return
        cur = self.Head
        while cur.next is not None:
            cur = cur.next
        cur.next = node

    def print_list(self):
        items = []
        cur = self.Head
        while cur is not None:
            items.append(str(cur.Element))
            cur = cur.next
        print(" ".join(items))

    def length(self):
        count = 0
        cur = self.Head
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def count(self, x):
        total = 0
        cur = self.Head
        while cur is not None:
            if cur.Element == x:
                total += 1
            cur = cur.next
        return total

    def find_max(self):
        if self.Head is None:
            return None
        biggest = self.Head.Element
        cur = self.Head.next
        while cur is not None:
            if cur.Element > biggest:
                biggest = cur.Element
            cur = cur.next
        return biggest

    def get_nth(self, n):
        if n < 0:
            print("Index out of range")
            return None
        cur = self.Head
        i = 0
        while cur is not None:
            if i == n:
                return cur.Element
            cur = cur.next
            i += 1
        print("Index out of range")
        return None


L = LL()
L.append(4); L.append(9); L.append(4); L.append(1)
L.print_list()
print(L.length(), L.count(4), L.find_max(), L.get_nth(2))
L.get_nth(2)