class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None


class LL:
    def __init__(self):
        self.Head = None

    def append(self, x):
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

    def search(self, x):
        """Position of first occurrence of x, or -1."""
        cur = self.Head
        i = 0
        while cur:
            if cur.Element == x:
                return i
            cur = cur.next
            i += 1
        return -1

    def delete_element(self, x):
        """Delete all occurrences of x."""
        # 1) remove matching nodes at the head (handles runs like 7 -> 7)
        while self.Head and self.Head.Element == x:
            self.Head = self.Head.next
        # 2) remove matching nodes after the head
        cur = self.Head
        while cur and cur.next:
            if cur.next.Element == x:
                cur.next = cur.next.next   # don't advance: next node may match too
            else:
                cur = cur.next


if __name__ == "__main__":
    L = LL()
    for v in [1, 1, 2, 1, 3]:
        L.append(v)
    print(L.search(2))
    print(L.search(5))
    L.delete_element(1)
    L.print_list()

    # edge case
    E = LL()
    E.append(7); E.append(7)
    E.delete_element(7)
    E.print_list()      # prints an empty line
    print(E.Head)       # None
