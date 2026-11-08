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
        current = self.Head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def print_list(self):
        """Print all elements in order."""
        elements = []
        current = self.Head
        while current is not None:
            elements.append(str(current.Element))
            current = current.next
        print(" ".join(elements))

    def length(self):
        """Return the number of nodes."""
        count = 0
        current = self.Head
        while current is not None:
            count += 1
            current = current.next
        return count

    def count(self, x):
        """Return how many times x appears."""
        cnt = 0
        current = self.Head
        while current is not None:
            if current.Element == x:
                cnt += 1
            current = current.next
        return cnt

    def find_max(self):
        """Return the largest element (None if empty)."""
        if self.Head is None:
            return None
        max_val = self.Head.Element
        current = self.Head.next
        while current is not None:
            if current.Element > max_val:
                max_val = current.Element
            current = current.next
        return max_val

    def get_nth(self, n):
        """Return the element at position n (0-indexed); print error if out of range."""
        current = self.Head
        idx = 0
        while current is not None:
            if idx == n:
                return current.Element
            current = current.next
            idx += 1
        print("Index out of range")

# Test case
if __name__ == "__main__":
    L = LL()
    L.append(4); L.append(9); L.append(4); L.append(1)
    L.print_list()
    print(L.length(), L.count(4), L.find_max(), L.get_nth(2))
    L.get_nth(10)