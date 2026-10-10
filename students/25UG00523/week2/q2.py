
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

    def search(self, x):
        current = self.Head
        index = 0

        while current is not None:
            if current.Element == x:
                return index

            current = current.next
            index += 1

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

    def print_list(self):
        current = self.Head

        while current is not None:
            print(current.Element, end=" ")
            current = current.next

        print()

if __name__ == "__main__":
    linked_list = LL()

    for value in [10, 20, 10, 30, 10, 40]:
        linked_list.append(value)

    print("Original list:")
    linked_list.print_list()

    print("Index of 30:", linked_list.search(30))
    print("Index of 50:", linked_list.search(50))

    linked_list.delete_element(10)

    print("After deleting all 10s:")
    linked_list.print_list()