class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None


class LL:
    def __init__(self):
        self.Head = None

    def add_element(self, x):
        """Insert x at the head."""
        n = Node(x)
        n.next = self.Head
        self.Head = n

    def append(self, x):
        """Insert x at the tail."""
        n = Node(x)
        if self.Head is None:
            self.Head = n
            return
        cur = self.Head
        while cur.next:
            cur = cur.next
        cur.next = n

    def print_list(self):
        items = []
        cur = self.Head
        while cur:
            items.append(str(cur.Element))
            cur = cur.next
        print(" ".join(items))

    def length(self):
        c = 0
        cur = self.Head
        while cur:
            c += 1
            cur = cur.next
        return c

    def count(self, x):
        c = 0
        cur = self.Head
        while cur:
            if cur.Element == x:
                c += 1
            cur = cur.next
        return c

    def find_max(self):
        if self.Head is None:
            return None
        m = self.Head.Element
        cur = self.Head.next
        while cur:
            if cur.Element > m:
                m = cur.Element
            cur = cur.next
        return m

    def get_nth(self, n):
        if n < 0:
            print("Index out of range")
            return None
        cur = self.Head
        i = 0
        while cur:
            if i == n:
                return cur.Element
            cur = cur.next
            i += 1
        print("Index out of range")
        return None


if __name__ == "__main__":
    L = LL()
    L.append(4); L.append(9); L.append(4); L.append(1)
    L.print_list()
    print(L.length(), L.count(4), L.find_max(), L.get_nth(2))
    L.get_nth(10)
