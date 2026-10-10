class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None


class LL:
    def __init__(self):
        self.Head = None

    def append(self, x):
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

    def search(self, x):
        cur = self.Head
        pos = 0
        while cur is not None:
            if cur.Element == x:
                return pos
            cur = cur.next
            pos += 1
        return -1

    def delete_element(self, x):
        # remove matching nodes at the head (handles "7 -> 7")
        while self.Head is not None and self.Head.Element == x:
            self.Head = self.Head.next
        # remove matching nodes in the rest of the list
        cur = self.Head
        while cur is not None and cur.next is not None:
            if cur.next.Element == x:
                cur.next = cur.next.next   # skip it, stay on cur
            else:
                cur = cur.next


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
E.print_list()   