
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
        while current is not None:
            print(current.Element, end=" ")
            current = current.next
        print()

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


# Testing Question 2
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

# Test deleting consecutive head elements
L2 = LL()
L2.append(7)
L2.append(7)
L2.delete_element(7)
L2.print_list()
