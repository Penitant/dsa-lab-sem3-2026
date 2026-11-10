
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
            print(current.Element, end=" ")
            current = current.next
        print()


def merge_sorted(L1, L2):
    result = LL()

    p = L1.Head
    q = L2.Head

    # Dummy node simplifies linking
    dummy = Node(0)
    tail = dummy

    while p is not None and q is not None:
        if p.Element <= q.Element:
            tail.next = p
            p = p.next
        else:
            tail.next = q
            q = q.next

        tail = tail.next

    # Attach remaining nodes
    if p is not None:
        tail.next = p
    else:
        tail.next = q

    result.Head = dummy.next
    return result


# Test
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

# Edge case: empty list
E = LL()
L3 = LL()
L3.append(5)
L3.append(6)

M2 = merge_sorted(E, L3)
M2.print_list()
