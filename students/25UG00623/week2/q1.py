
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
            print(current.Element, end=" ")
            current = current.next
        print()

    def length(self):
        count = 0
        current = self.Head
        while current is not None:
            count += 1
            current = current.next
        return count

    def count(self, x):
        total = 0
        current = self.Head
        while current is not None:
            if current.Element == x:
                total += 1
            current = current.next
        return total

    def find_max(self):
        if self.Head is None:
            return None

        maximum = self.Head.Element
        current = self.Head.next
        while current is not None:
            if current.Element > maximum:
                maximum = current.Element
            current = current.next
        return maximum

    def get_nth(self, n):
        if n < 0:
            print("Index out of range")
            return

        current = self.Head
        index = 0
        while current is not None:
            if index == n:
                return current.Element
            current = current.next
            index += 1

        print("Index out of range")


# Testing Question 1
L = LL()
L.append(4)
L.append(9)
L.append(4)
L.append(1)

L.print_list()
L.add_element(4)
L.print_list()
L.get_nth(10)
