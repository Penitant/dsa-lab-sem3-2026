class Job:
    def __init__(self, name, priority, submitted):
        self.name = name
        self.priority = priority
        self.submitted = submitted

    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.submitted > other.submitted


def parent(i):
    return (i - 1) / 2


def left(i):
    return 2 * i + 1


def right(i):
    return 2 * i + 2


class GPUQueue:
    def __init__(self):
        self.h = []

    def sift_up(self, i):
        while i > 0 and self.h[i] < self.h[parent(i)]:
            p = parent(i)
            self.h[i], self.h[p] = self.h[p], self.h[i]
            i = p

    def sift_down(self, i):
        n = len(self.h)
        while left(i) < n:
            c = left(i)
            if right(i) < n and self.h[c] < self.h[right(i)]:
                c = right(i)
            if self.h[c] < self.h[i]:
                self.h[i], self.h[c] = self.h[c], self.h[i]
                i = c
            else:
                break
