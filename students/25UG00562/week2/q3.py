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

    # Start from the heads of both lists
    first = L1.Head
    second = L2.Head

    # Create a dummy node to simplify merging
    dummy = Node(0)
    tail = dummy

    # Compare elements and link the smaller node
    while first is not None and second is not None:
        if first.Element <= second.Element:
            tail.next = first
            first = first.next
        else:
            tail.next = second
            second = second.next

        tail = tail.next

    # Attach any remaining nodes
    if first is not None:
        tail.next = first

    if second is not None:
        tail.next = second

    result.Head = dummy.next
    return result


# Test Q3
if __name__ == "__main__":
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

    # Edge case: merging an empty list
    L3 = LL()

    L4 = LL()
    L4.append(5)
    L4.append(6)

    merged2 = merge_sorted(L3, L4)
    merged2.print_list()
