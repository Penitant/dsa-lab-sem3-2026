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

        current = self.Head
        while current.next is not None:
            current = current.next

        current.next = new_node

    def print_list(self):
        current = self.Head

        while current is not None:
            print(current.Element, end="")
            if current.next is not None:
                print(" ", end="")
            current = current.next

        print()


def merge_sorted(L1, L2):
    result = LL()

    p = L1.Head
    q = L2.Head

    # Temporary starting node simplifies linking.
    dummy = Node(None)
    tail = dummy

    while p is not None and q is not None:
        if p.Element <= q.Element:
            selected = p
            p = p.next
        else:
            selected = q
            q = q.next

        tail.next = selected
        tail = selected

    # Attach whichever list still has nodes.
    if p is not None:
        tail.next = p
    else:
        tail.next = q

    result.Head = dummy.next
    return result


# Test Q3
if __name__ == "__main__":
    L1 = LL()
    for value in [1, 4, 7]:
        L1.append(value)

    L2 = LL()
    for value in [2, 3, 8]:
        L2.append(value)

    M = merge_sorted(L1, L2)
    M.print_list()

    # Edge case: one empty list.
    empty = LL()
    other = LL()
    other.append(5)
    other.append(6)

    merged = merge_sorted(empty, other)
    merged.print_list()

    # Edge case: both lists empty.
    empty_result = merge_sorted(LL(), LL())
    empty_result.print_list()