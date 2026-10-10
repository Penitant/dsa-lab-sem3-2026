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

    @classmethod
    def from_string(cls, s):
        number = cls()

        # Store digits from right to left.
        for ch in reversed(s):
            number.append(int(ch))

        # Remove unnecessary leading zeros in the input.
        while (
            number.Head is not None
            and number.Head.Element == 0
            and number.Head.next is not None
        ):
            number.Head = number.Head.next

        return number

    def to_string(self):
        digits = []
        current = self.Head

        while current is not None:
            digits.append(str(current.Element))
            current = current.next

        if not digits:
            return "0"

        # Digits are stored least significant first.
        result = "".join(reversed(digits))

        # Ensure zero is represented as "0".
        result = result.lstrip("0")
        return result if result else "0"


def add(A, B):
    result = LL()

    p = A.Head
    q = B.Head
    carry = 0

    while p is not None or q is not None or carry:
        a = p.Element if p is not None else 0
        b = q.Element if q is not None else 0

        total = a + b + carry
        result.append(total % 10)
        carry = total // 10

        if p is not None:
            p = p.next
        if q is not None:
            q = q.next

    if result.Head is None:
        result.append(0)

    return result


def subtract(A, B):
    # Assumes A >= B.
    result = LL()

    p = A.Head
    q = B.Head
    borrow = 0

    while p is not None:
        a = p.Element - borrow
        b = q.Element if q is not None else 0

        if a < b:
            a += 10
            borrow = 1
        else:
            borrow = 0

        result.append(a - b)

        p = p.next
        if q is not None:
            q = q.next

    # Remove unnecessary zeros from the most significant end.
    if result.Head is None:
        result.append(0)
    else:
        current = result.Head
        last_nonzero = None

        while current is not None:
            if current.Element != 0:
                last_nonzero = current
            current = current.next

        if last_nonzero is None:
            result.Head = Node(0)
        else:
            last_nonzero.next = None

    return result


# Test cases
if __name__ == "__main__":
    A = LL.from_string("999999999999")
    B = LL.from_string("1")
    print(add(A, B).to_string())

    A = LL.from_string("12345")
    B = LL.from_string("678")
    print(add(A, B).to_string())

    A = LL.from_string("1000")
    B = LL.from_string("999")
    print(subtract(A, B).to_string())

    A = LL.from_string("500")
    B = LL.from_string("500")
    print(subtract(A, B).to_string())