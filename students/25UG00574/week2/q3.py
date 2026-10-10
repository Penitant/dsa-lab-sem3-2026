"""Q3. Merge Two Sorted Lists"""


class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None


class LL:
    def __init__(self):
        self.Head = None

    def append(self, x):
        new_node = Node(x)
        if self.Head is None:
            self.Head = new_node
            return
        cur = self.Head
        while cur.next is not None:
            cur = cur.next
        cur.next = new_node

    def print_list(self):
        items = []
        cur = self.Head
        while cur is not None:
            items.append(str(cur.Element))
            cur = cur.next
        print(" ".join(items))


def merge_sorted(L1, L2):
    merged = LL()
    tail = None          # last node of the merged list
    a = L1.Head
    b = L2.Head

    while a is not None or b is not None:
        # pick the smaller node (or whichever list still has nodes)
        if b is None or (a is not None and a.Element <= b.Element):
            chosen = a
            a = a.next
        else:
            chosen = b
            b = b.next

        # link the chosen node at the end of the merged list
        if tail is None:
            merged.Head = chosen
        else:
            tail.next = chosen
        tail = chosen

    return merged


if __name__ == "__main__":
    # L1 = 1 -> 4 -> 7
    L1 = LL()
    for v in [1, 4, 7]:
        L1.append(v)
    # L2 = 2 -> 3 -> 8
    L2 = LL()
    for v in [2, 3, 8]:
        L2.append(v)
    M = merge_sorted(L1, L2)
    M.print_list()

    # Edge case: empty list + 5 -> 6
    E = LL()
    F = LL()
    F.append(5); F.append(6)
    merge_sorted(E, F).print_list()
