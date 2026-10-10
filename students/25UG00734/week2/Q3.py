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


def merge_sorted(L1, L2):
    result = LL()
    tail = None

    a = L1.Head
    b = L2.Head
    while a is not None or b is not None:
        # pick the smaller front node (or whichever list still has nodes)
        if b is None or (a is not None and a.Element <= b.Element):
            node = Node(a.Element)
            a = a.next
        else:
            node = Node(b.Element)
            b = b.next

        # link the new node at the tail of the result
        if tail is None:
            result.Head = node
        else:
            tail.next = node
        tail = node

    return result


L1 = LL()
for v in [1, 4, 7]:
    L1.append(v)
L2 = LL()
for v in [2, 3, 8]:
    L2.append(v)
M = merge_sorted(L1, L2)
M.print_list()

# edge case
empty = LL()
F = LL()
F.append(5); F.append(6)
merge_sorted(empty, F).print_list()