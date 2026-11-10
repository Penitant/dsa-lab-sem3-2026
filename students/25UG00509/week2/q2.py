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

    def search(self, x):
        """Return the position (0-indexed) of the first occurrence of x, or -1."""
        current = self.Head
        pos = 0
        while current is not None:
            if current.Element == x:
                return pos
            current = current.next
            pos += 1
        return -1

    def delete_element(self, x):
        """Delete all occurrences of x."""
        # Remove matching nodes from the head
        while self.Head is not None and self.Head.Element == x:
            self.Head = self.Head.next

        current = self.Head
        while current is not None and current.next is not None:
            if current.next.Element == x:
                current.next = current.next.next
            else:
                current = current.next

# Test case
if __name__ == "__main__":
    L = LL()
    for val in [1, 1, 2, 1, 3]:
        L.append(val)
    print(L.search(2))
    print(L.search(5))
    L.delete_element(1)
    L.print_list()