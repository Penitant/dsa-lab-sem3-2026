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

        while current is not None:
            count += 1
            current = current.next

        return count

    # 5. Return how many times x appears
    def count(self, x):
        count = 0
        current = self.head

        while current is not None:
            if current.data == x:
                count += 1
            current = current.next

        return count

    # 6. Return largest element
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

    # 7. Return element at position n
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


# Example
ll = LL()

ll.add_element(10)
ll.add_element(20)
ll.append(30)
ll.append(40)
ll.append(30)

ll.print_list()

print("Length:", ll.length())
print("Count of 30:", ll.count(30))
print("Maximum:", ll.find_max())
print("Element at position 2:", ll.get_nth(2))
print("Element at position 10:", ll.get_nth(10))

