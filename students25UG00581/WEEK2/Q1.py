class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LL:
    def __init__(self):
        self.head = None

    # 1. Insert x at the head
    def add_element(self, x):
        new_node = Node(x)
        new_node.next = self.head
        self.head = new_node

    # 2. Insert x at the tail
    def append(self, x):
        new_node = Node(x)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node

    # 3. Print all elements
    def print_list(self):
        current = self.head

        while current is not None:
            print(current.data, end=" ")
            current = current.next

        print()

    # 4. Return number of nodes
    def length(self):
        count = 0
        current = self.head
