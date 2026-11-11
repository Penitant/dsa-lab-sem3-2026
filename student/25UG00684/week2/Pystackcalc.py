class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None

class LL:
    def __init__(self):
        self.Head = None

    def add_element(self, x):
        """Insert x at the head."""
        new_node = Node(x)
        new_node.next = self.Head
        self.Head = new_node

    def append(self, x):
        """Insert x at the tail."""
        new_node = Node(x)
        if self.Head is None:
            self.Head = new_node
            return
        curr = self.Head
        while curr.next is not None:
            curr = curr.next
        curr.next = new_node

    def print_list(self):
        """Print all elements in order separated by spaces."""
        curr = self.Head
        elements = []
        while curr is not None:
            elements.append(str(curr.Element))
            curr = curr.next
        print(" ".join(elements))

    def length(self):
        """Return the number of nodes."""
        count = 0
        curr = self.Head
        while curr is not None:
            count += 1
            curr = curr.next
        return count

    def count(self, x):
        """Return how many times x appears."""
        c = 0
        curr = self.Head
        while curr is not None:
            if curr.Element == x:
                c += 1
            curr = curr.next
        return c

    def find_max(self):
        """Return the largest element (None if empty)."""
        if self.Head is None:
            return None
        max_val = self.Head.Element
        curr = self.Head.next
        while curr is not None:
            if curr.Element > max_val:
                max_val = curr.Element
            curr = curr.next
        return max_val

    def get_nth(self, n):
        """Return the element at position n (0-indexed); print error if out of range."""
        curr = self.Head
        idx = 0
        while curr is not None:
            if idx == n:
                return curr.Element
            curr = curr.next
            idx += 1
        print("Index out of range")

if __name__ == "__main__":
    L = LL()
    L.append(4); L.append(9); L.append(4); L.append(1)
    L.print_list()
    print(L.length(), L.count(4), L.find_max(), L.get_nth(2))
    L.get_nth(10)
