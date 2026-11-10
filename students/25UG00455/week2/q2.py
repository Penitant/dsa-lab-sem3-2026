
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
        current = self.Head
        elements = []

        while current is not None:
            elements.append(str(current.Element))
            current = current.next

        print(" ".join(elements))

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
        while self.Head is not None and self.Head.Element == x:
            self.Head = self.Head.next

        current = self.Head

        while current is not None and current.next is not None:
            if current.next.Element == x:
                current.next = current.next.next
            else:
                current = current.next


if __name__ == "__main__":
    L = LL()
    L.append(1)
    L.append(1)
    L.append(2)
    L.append(1)
    L.append(3)

    print(L.search(2))
    print(L.search(5))

    L.delete_element(1)
    L.print_list()

    # Edge case: deleting every node
    E = LL()
    E.append(7)
    E.append(7)
    E.delete_element(7)
    E.print_list()
