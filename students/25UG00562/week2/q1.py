
class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None


class LL:
    def __init__(self):
        self.Head = None

    # Insert at the beginning
    def add_element(self, x):
        new_node = Node(x)
        new_node.next = self.Head
        self.Head = new_node

    # Insert at the end
    def append(self, x):
        new_node = Node(x)

        if self.Head is None:
            self.Head = new_node
            return

        current = self.Head

        while current.next is not None:
            current = current.next

        current.next = new_node

    # Print all elements
    def print_list(self):
        current = self.Head
        elements = []

        while current is not None:
            elements.append(str(current.Element))
            current = current.next

        print(" ".join(elements))

    # Count the number of nodes
    def length(self):
        count = 0
        current = self.Head

        while current is not None:
            count += 1
            current = current.next

        return count

    # Count occurrences of x
    def count(self, x):
        count = 0
        current = self.Head

        while current is not None:
            if current.Element == x:
                count += 1
            current = current.next

        return count

    # Find the largest element
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

    # Get element at position n (0-indexed)
    def get_nth(self, n):
        if n < 0:
            print("Index out of range")
            return None

        current = self.Head
        position = 0

        while current is not None:
            if position == n:
                return current.Element

            current = current.next
            position += 1

        print("Index out of range")
        return None


# Test Q1
if __name__ == "__main__":
    L = LL()
    L.append(4)
    L.append(9)
    L.append(4)
    L.append(1)

    L.print_list()
    print(L.length(), L.count(4), L.find_max(), L.get_nth(2))
    L.get_nth(10)
