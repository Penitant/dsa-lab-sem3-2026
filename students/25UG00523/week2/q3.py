
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

    # Use a dummy node to build the merged list
    dummy = Node(0)
    tail = dummy

    while p is not None and q is not None:
        if p.Element <= q.Element:
            tail.next = Node(p.Element)
            p = p.next
        else:
            tail.next = Node(q.Element)
            q = q.next

        tail = tail.next

    while p is not None:
        tail.next = Node(p.Element)
        tail = tail.next
        p = p.next

    while q is not None:
        tail.next = Node(q.Element)
        tail = tail.next
        q = q.next

    result.Head = dummy.next
    return result

if __name__ == "__main__":
    L1 = LL()
    L2 = LL()

    for value in [10, 30, 50]:
        L1.append(value)

    for value in [20, 40, 60]:
        L2.append(value)

    print("List 1:")
    L1.print_list()

    print("List 2:")
    L2.print_list()

    merged = merge_sorted(L1, L2)

    print("Merged list:")
    merged.print_list()