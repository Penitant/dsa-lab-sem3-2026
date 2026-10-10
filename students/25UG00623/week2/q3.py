
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
    tail = None

    while p is not None and q is not None:
        if p.Element <= q.Element:
            node = p
            p = p.next
        else:
            node = q
            q = q.next

        if result.Head is None:
            result.Head = node
        else:
            tail.next = node

        tail = node

    if p is not None:
        if result.Head is None:
            result.Head = p
        else:
            tail.next = p
    elif q is not None:
        if result.Head is None:
            result.Head = q
        else:
            tail.next = q

    return result


# Testing Question 3
L1 = LL()
L1.append(1)
L1.append(4)
L1.append(7)

L2 = LL()
L2.append(2)
L2.append(3)
L2.append(8)

merged = merge_sorted(L1, L2)
merged.print_list()

# Test with an empty list
L3 = LL()
L4 = LL()
L4.append(5)
L4.append(6)

merged2 = merge_sorted(L3, L4)
merged2.print_list()
