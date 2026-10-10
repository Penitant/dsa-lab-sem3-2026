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

    def search(self, x):
        """Position of the first occurrence of x, or -1 if not found."""
        cur = self.Head
        i = 0
        while cur is not None:
            if cur.Element == x:
                return i
            cur = cur.next
            i += 1
        return -1

    def delete_element(self, x):
        """Delete all occurrences of x."""
        # Step 1: remove matching nodes at the head (handles runs like 7 -> 7)
        while self.Head is not None and self.Head.Element == x:
            self.Head = self.Head.next
        # Step 2: remove matching nodes in the rest of the list
        cur = self.Head
        while cur is not None and cur.next is not None:
            if cur.next.Element == x:
                cur.next = cur.next.next   # skip it; stay on cur since the next one may match too
            else:
                cur = cur.next


if __name__ == "__main__":
    L = LL()
    for v in (1, 1, 2, 1, 3):
        L.append(v)
    print(L.search(2))
    print(L.search(5))
    L.delete_element(1)
    L.print_list()

    # edge case: 7 -> 7
    E = LL()
    E.append(7); E.append(7)
    E.delete_element(7)
    E.print_list()   # prints an empty line
