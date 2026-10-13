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
        curr = self.Head
        while curr.next is not None:
            curr = curr.next
        curr.next = new_node

    def print_list(self):
        curr = self.Head
        elements = []
        while curr is not None:
            elements.append(str(curr.Element))
            curr = curr.next
        print(" ".join(elements))

def merge_sorted(L1, L2):
    """Merge two sorted linked lists by walking through and linking nodes."""
    dummy = Node(0)
    tail = dummy
    p1 = L1.Head
    p2 = L2.Head

    while p1 is not None and p2 is not None:
        if p1.Element <= p2.Element:
            tail.next = p1
            p1 = p1.next
        else:
            tail.next = p2
            p2 = p2.next
        tail = tail.next

    # Attach remaining elements
    if p1 is not None:
        tail.next = p1
    elif p2 is not None:
        tail.next = p2

    merged_ll = LL()
    merged_ll.Head = dummy.next
    return merged_ll

if __name__ == "__main__":
    L1 = LL()
    L1.append(1); L1.append(4); L1.append(7)
    
    L2 = LL()
    L2.append(2); L2.append(3); L2.append(8)

    M = merge_sorted(L1, L2)
    M.print_list()
