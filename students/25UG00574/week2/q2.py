"""Q2. Search and Delete"""


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
        cur = self.Head
        while cur.next is not None:
            cur = cur.next
        cur.next = new_node

    def print_list(self):
        items = []
        cur = self.Head
        while cur is not None:
            items.append(str(cur.Element))
            cur = cur.next
        print(" ".join(items))

    # position (0-indexed) of first x, or -1
    def search(self, x):
        cur = self.Head
        index = 0
        while cur is not None:
            if cur.Element == x:
                return index
            cur = cur.next
            index += 1
        return -1

    # delete ALL occurrences of x
    def delete_element(self, x):
        # 1. remove x from the front (handles 7 -> 7 and head deletes)
        while self.Head is not None and self.Head.Element == x:
            self.Head = self.Head.next
        # 2. remove x from the rest of the list
        cur = self.Head
        while cur is not None and cur.next is not None:
            if cur.next.Element == x:
                cur.next = cur.next.next   # skip the node
            else:
                cur = cur.next


if __name__ == "__main__":
    # L = 1 -> 1 -> 2 -> 1 -> 3
    L = LL()
    for v in [1, 1, 2, 1, 3]:
        L.append(v)
    print(L.search(2))
    print(L.search(5))
    L.delete_element(1)
    L.print_list()

    # Edge case: deleting 7 from 7 -> 7 leaves an empty list
    E = LL()
    E.append(7); E.append(7)
    E.delete_element(7)
    print(E.Head is None)   # True -> empty list
