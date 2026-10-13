
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
        elements = []

        while current is not None:
            elements.append(str(current.Element))
            current = current.next

        print(" ".join(elements))


def merge_sorted(L1, L2):
    merged = LL()
    dummy = Node(None)
    tail = dummy

    first = L1.Head
    second = L2.Head

    while first is not None and second is not None:
        if first.Element <= second.Element:
            tail.next = first
            first = first.next
        else:
            tail.next = second
            second = second.next

        tail = tail.next

    if first is not None:
        tail.next = first
    else:
        tail.next = second

    merged.Head = dummy.next
    return merged


if __name__ == "__main__":
    L1 = LL()
    L1.append(1)
    L1.append(4)
    L1.append(7)

    L2 = LL()
    L2.append(2)
    L2.append(3)
    L2.append(8)

    M = merge_sorted(L1, L2)
    M.print_list()

    E = LL()
    E.append(5)
    E.append(6)

    empty = LL()
    merged_edge = merge_sorted(empty, E)
    merged_edge.print_list()
