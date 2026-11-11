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

    def search(self, x):
        """Return position (0-indexed) of first occurrence of x, or -1 if not found."""
        curr = self.Head
        idx = 0
        while curr is not None:
            if curr.Element == x:
                return idx
            curr = curr.next
            idx += 1
        return -1

    def delete_element(self, x):
        """Delete all occurrences of x (including consecutive/head occurrences)."""
        # Remove matching nodes from the head
        while self.Head is not None and self.Head.Element == x:
            self.Head = self.Head.next

        # Remove matching nodes from the rest of the list
        curr = self.Head
        while curr is not None and curr.next is not None:
            if curr.next.Element == x:
                curr.next = curr.next.next
            else:
                curr = curr.next

if __name__ == "__main__":
    L = LL()
    L.append(1); L.append(1); L.append(2); L.append(1); L.append(3)
    print(L.search(2))
    print(L.search(5))
    L.delete_element(1)
    L.print_list()
