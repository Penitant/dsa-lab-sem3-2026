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


def merge_sorted(L1, L2):
    """Merge two sorted linked lists into a new sorted LL (inputs untouched)."""
    result = LL()
    tail = None

    def add(value):
        nonlocal tail
        n = Node(value)
        if tail is None:
            result.Head = n
        else:
            tail.next = n
        tail = n

    a, b = L1.Head, L2.Head
    while a and b:
        if a.Element <= b.Element:
            add(a.Element)
            a = a.next
        else:
            add(b.Element)
            b = b.next
    while a:            # leftovers from L1
        add(a.Element)
        a = a.next
    while b:            # leftovers from L2
        add(b.Element)
        b = b.next
    return result


if __name__ == "__main__":
    L1, L2 = LL(), LL()
    for v in [1, 4, 7]:
        L1.append(v)
    for v in [2, 3, 8]:
        L2.append(v)
    merge_sorted(L1, L2).print_list()

    # edge case: empty + (5 -> 6)
    E, F = LL(), LL()
    F.append(5); F.append(6)
    merge_sorted(E, F).print_list()
