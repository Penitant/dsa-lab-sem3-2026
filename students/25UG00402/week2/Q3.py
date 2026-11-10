class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None
class LL:
    def __init__(self):
        self.Head = None
    def add_element(self, x):
        new_node = Node(x)
        new_node.next = self.Head
        self.Head = new_node
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
    tail = None
    first = L1.Head
    second = L2.Head
    while first is not None and second is not None:
        if first.Element <= second.Element:
            value = first.Element
            first = first.next
        else:
            value = second.Element
            second = second.next
        new_node = Node(value)
        if merged.Head is None:
            merged.Head = new_node
        else:
            tail.next = new_node
        tail = new_node
    while first is not None:
        new_node = Node(first.Element)
        if merged.Head is None:
            merged.Head = new_node
        else:
            tail.next = new_node
        tail = new_node
        first = first.next
    while second is not None:
        new_node = Node(second.Element)
        if merged.Head is None:
            merged.Head = new_node
        else:
            tail.next = new_node
        tail = new_node
        second = second.next
    return merged
if __name__ == "__main__":
    L1 = LL()
    L2 = LL()
    for value in [1, 4, 7]:
        L1.append(value)
    for value in [2, 3, 8]:
        L2.append(value)
    M = merge_sorted(L1, L2)
    M.print_list()
    empty = LL()
    other = LL()
    other.append(5)
    other.append(6)
    merge_sorted(empty, other).print_list()