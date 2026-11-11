class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LL:
    def __init__(self):
        self.head = None

    def append(self, x):
        new_node = Node(x)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node

    def print_list(self):
        current = self.head

        while current is not None:
            print(current.data, end=" ")
            current = current.next

        print()


def merge_sorted(L1, L2):
    M = LL()

    p = L1.head
    q = L2.head

    # Temporary dummy node
    dummy = Node(0)
    current = dummy

    # Compare both lists
    while p is not None and q is not None:

        if p.data <= q.data:
            current.next = p
            p = p.next
        else:
            current.next = q
            q = q.next

        current = current.next

    # If L1 still has nodes
    if p is not None:
        current.next = p

    # If L2 still has nodes
    if q is not None:
        current.next = q

    M.head = dummy.next

    return M


# L1 = 1 -> 4 -> 7
L1 = LL()
L1.append(1)
L1.append(4)
L1.append(7)

# L2 = 2 -> 3 -> 8
L2 = LL()
L2.append(2)
L2.append(3)
L2.append(8)

# Merge
M = merge_sorted(L1, L2)

M.print_list()

