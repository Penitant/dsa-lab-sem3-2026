
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
            raise IndexError("Index out of range")

        current = self.Head
        index = 0

        while current is not None:
            if index == n:
                return current.Element

            current = current.next
            index += 1

        raise IndexError("Index out of range")

if __name__ == "__main__":
    linked_list = LL()

    linked_list.append(10)
    linked_list.append(20)
    linked_list.append(30)
    linked_list.add_element(5)

    print("Linked list:")
    linked_list.print_list()
    print("Length:", linked_list.length())
    print("Count of 20:", linked_list.count(20))
    print("Maximum:", linked_list.find_max())
    print("Element at index 2:", linked_list.get_nth(2))