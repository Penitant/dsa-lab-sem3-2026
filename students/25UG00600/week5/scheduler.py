class Job:
    def __init__(self, name, priority, submitted):
        self.name = name
        self.priority = priority
        self.submitted = submitted

    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority < other.priority
        # FIX 2: on equal priority the job submitted FIRST (smaller number) runs first
        return self.submitted < other.submitted


def parent(i):
    # FIX 1: index must be an integer, so use integer division (//) not /
    return (i - 1) // 2


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
            # FIX 3: pick the SMALLER child (the one that should run first)
            if right(i) < n and self.h[right(i)] < self.h[c]:
                c = right(i)
            if self.h[c] < self.h[i]:
                self.h[i], self.h[c] = self.h[c], self.h[i]
                i = c
            else:
                break

    def submit(self, job):
        self.h.append(job)
        self.sift_up(len(self.h) - 1)

    def next_job(self):
        if len(self.h) == 0:
            return None
        top = self.h[0]
        # FIX 4: pop the last job first; if the heap is now empty there is
        # nothing to move to the root (the old code crashed with one job left)
        last = self.h.pop()
        if len(self.h) > 0:
            self.h[0] = last
            self.sift_down(0)
        return top

    # FIX 5: the colon after the parameter list was missing (syntax error)
    def cancel(self, name):
        for i in range(len(self.h)):
            if self.h[i].name == name:
                last = self.h.pop()
                if i < len(self.h):
                    self.h[i] = last
                    # FIX 6: the moved job may need to go UP or DOWN
                    self.sift_up(i)
                    self.sift_down(i)
                return True
        return False


def main():
    q = GPUQueue()
    n = int(input())
    submitted = 0
    for _ in range(n):
        parts = input().split()
        if parts[0] == "SUBMIT":
            submitted += 1
            q.submit(Job(parts[1], int(parts[2]), submitted))
        elif parts[0] == "RUN":
            job = q.next_job()
            if job is None:
                print("GPU idle")
            else:
                print(job.name)
        elif parts[0] == "CANCEL":
            if not q.cancel(parts[1]):
                print(parts[1], "not found")


main()
