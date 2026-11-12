class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LL:
    def __init__(self):
        self.head = None

    def add_element(self, x):
        new_node = Node(x)
        new_node.next = self.head
        self.head = new_node

    def append(self, x):
        new_node = Node(x)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node

    def print_list(self):
        current = self.head

        while current is not None:
            print(current.data, end=" ")
            current = current.next

        print()

    def length(self):
        count = 0
        current = self.head

        while current is not None:
            count += 1
            current = current.next

        return count

    def count(self, x):
        count = 0
        current = self.head

        while current is not None:
            if current.data == x:
                count += 1
            current = current.next

        return count

    def find_max(self):
        if self.head is None:
            return None

        maximum = self.head.data
        current = self.head.next

        while current is not None:
            if current.data > maximum:
                maximum = current.data
            current = current.next

        return maximum

    def get_nth(self, n):
        if n < 0:
            print("Error: index out of range")
            return None

        current = self.head
        index = 0

        while current is not None:
            if index == n:
                return current.data

            current = current.next
            index += 1

        print("Error: index out of range")
        return None

    # Q2 - Search
    def search(self, x):
        current = self.head
        index = 0

        while current is not None:
            if current.data == x:
                return index

            current = current.next
            index += 1

        return -1

    # Q2 - Delete all occurrences
    def delete_element(self, x):
        while self.head is not None and self.head.data == x:
            self.head = self.head.next

        current = self.head

        while current is not None and current.next is not None:
            if current.next.data == x:
                current.next = current.next.next
            else:
                current = current.next


# Test case
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
