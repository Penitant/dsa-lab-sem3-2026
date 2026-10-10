class Node:
    """One node of the singly linked list."""
    def __init__(self, initdata):
        self.Element = initdata   # the stored value
        self.next = None          # link to the next node (None = end of list)


class LL:
    """Singly linked list; Head points to the first node."""
    def __init__(self):
        self.Head = None          # empty list

    def add_element(self, x):
        """Insert x at the head."""
        n = Node(x)
        n.next = self.Head        # new node points to the old first node
        self.Head = n             # new node becomes the head

    def append(self, x):
        """Insert x at the tail."""
        n = Node(x)
        if self.Head is None:     # empty list: new node is the head
            self.Head = n
            return
        cur = self.Head
        while cur.next is not None:   # walk to the last node
            cur = cur.next
        cur.next = n

    def print_list(self):
        """Print all elements in order, space separated."""
        items = []
        cur = self.Head
        while cur is not None:
            items.append(str(cur.Element))
            cur = cur.next
        print(" ".join(items))

    def length(self):
        """Number of nodes."""
        count = 0
        cur = self.Head
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    def count(self, x):
        """How many times x appears."""
        total = 0
        cur = self.Head
        while cur is not None:
            if cur.Element == x:
                total += 1
            cur = cur.next
        return total

    def find_max(self):
        """Largest element, or None for an empty list."""
        if self.Head is None:
            return None
        best = self.Head.Element      # start with the first value
        cur = self.Head.next
        while cur is not None:
            if cur.Element > best:
                best = cur.Element
            cur = cur.next
        return best

    def get_nth(self, n):
        """Element at 0-indexed position n; prints an error if out of range."""
        if n < 0:
            print("Index out of range")
            return None
        cur = self.Head
        i = 0
        while cur is not None:
            if i == n:
                return cur.Element
            cur = cur.next
            i += 1
        print("Index out of range")   # ran past the end of the list
        return None


if __name__ == "__main__":
    L = LL()
    L.append(4); L.append(9); L.append(4); L.append(1)
    L.print_list()
    print(L.length(), L.count(4), L.find_max(), L.get_nth(2))
    L.get_nth(10)
