"""Q1. Build the List"""


class Node:
    def __init__(self, initdata):
        self.Element = initdata
        self.next = None


class LL:
    def __init__(self):
        self.Head = None

    # insert x at the head
    def add_element(self, x):
        new_node = Node(x)
        new_node.next = self.Head
        self.Head = new_node

    # insert x at the tail
    def append(self, x):
        new_node = Node(x)
        if self.Head is None:
            self.Head = new_node
            return
        cur = self.Head
        while cur.next is not None:
            cur = cur.next
        cur.next = new_node

    # print all elements in order
    def print_list(self):
        items = []
        cur = self.Head
        while cur is not None:
            items.append(str(cur.Element))
            cur = cur.next
        print(" ".join(items))

    # number of nodes
    def length(self):
        count = 0
        cur = self.Head
        while cur is not None:
            count += 1
            cur = cur.next
        return count

    # how many times x appears
    def count(self, x):
        total = 0
        cur = self.Head
        while cur is not None:
            if cur.Element == x:
                total += 1
            cur = cur.next
        return total

    # largest element (None if empty)
    def find_max(self):
        if self.Head is None:
            return None
        biggest = self.Head.Element
        cur = self.Head.next
        while cur is not None:
            if cur.Element > biggest:
                biggest = cur.Element
            cur = cur.next
        return biggest

    # element at position n (0-indexed)
    def get_nth(self, n):
        if n < 0:
            print("Index out of range")
            return None
        cur = self.Head
        index = 0
        while cur is not None:
            if index == n:
                return cur.Element
            cur = cur.next
            index += 1
        print("Index out of range")
        return None


if __name__ == "__main__":
    L = LL()
    L.append(4); L.append(9); L.append(4); L.append(1)
    L.print_list()
    print(L.length(), L.count(4), L.find_max(), L.get_nth(2))
    L.get_nth(10)
    
