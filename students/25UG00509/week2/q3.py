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
        elements = []
        current = self.Head
        while current is not None:
            elements.append(str(current.Element))
            current = current.next
        print(" ".join(elements))

def merge_sorted(L1, L2):
    """Merge two sorted linked lists into a new sorted LL."""
    merged_list = LL()
    
    # Dummy node to easily build the new list
    dummy = Node(0)
    tail = dummy
    
    p1 = L1.Head
    p2 = L2.Head
    
    while p1 is not None and p2 is not None:
        if p1.Element <= p2.Element:
            tail.next = Node(p1.Element)
            p1 = p1.next
        else:
            tail.next = Node(p2.Element)
            p2 = p2.next
        tail = tail.next
        
    # Attach remaining elements
    while p1 is not None:
        tail.next = Node(p1.Element)
        p1 = p1.next
        tail = tail.next
        
    while p2 is not None:
        tail.next = Node(p2.Element)
        p2 = p2.next
        tail = tail.next
        
    merged_list.Head = dummy.next
    return merged_list

# Test case
if __name__ == "__main__":
    L1 = LL()
    for x in [1, 4, 7]: L1.append(x)
    
    L2 = LL()
    for x in [2, 3, 8]: L2.append(x)
    
    M = merge_sorted(L1, L2)
    M.print_list()