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

        while current is not None:
            print(current.Element, end="")
            if current.next is not None:
                print(" ", end="")
            current = current.next

        print()

    def search(self, x):
        current = self.Head
        position = 0

        while current is not None:
            if current.Element == x:
                return position

            current = current.next
            position += 1

        return -1

    def delete_element(self, x):
        # Remove all matching nodes at the head.
        while self.Head is not None and self.Head.Element == x:
            self.Head = self.Head.next

        # Remove all matching nodes after the head.
        current = self.Head

        while current is not None and current.next is not None:
            if current.next.Element == x:
                current.next = current.next.next
            else:
                current = current.next


# Test Q2
if __name__ == "__main__":
    L = LL()

    for value in [1, 1, 2, 1, 3]:
        L.append(value)

    print(L.search(2))
    print(L.search(5))

    L.delete_element(1)
    L.print_list()

    # Edge case: deleting all nodes.
    E = LL()
    E.append(7)
    E.append(7)
    E.delete_element(7)
    E.print_list()