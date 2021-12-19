# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201
from math import log, floor
from rich import print
from itertools import product

def read_int():
    return int(input())

def read_int_array():
    return [int(ss) for ss in input().split()]


def simulate_1_heap():
    results = {0: False}
    def check(i):
        p2 = 1
        while p2 <= i:
            if not results[i - p2]:
                return True
            p2 *= 2
        return False
    for i in range(1, 100):
        results[i] = check(i)
    print(results)

# simulate_1_heap()
# Conclusion:
#   For a single heap, having a multiple of 3mp is Losing.
#   Anything else is a Win.

DEBUG = False

LOSE = set([
    (),
    (1, 1),
    (2, 2),
    (1, 1, 3),
    (3, 3, 3),
    ])
WIN = set([
    ])

#simulate_multiple_heaps():

def is_winning_situation(heaps):
    if len(heaps) == 0:
        return False
    if len(heaps) == 1:
        return heaps[1] % 3 > 0
    for i, h in enumerate(heaps):
        for p2 in range(0, floor(log(h, 2)) + 1):
            l = list(heaps)
            l[i] = h - 2**p2
            if l[i] == 0:
                l.pop(i)
            l.sort()
            t = tuple(l)
            if t in LOSE:
                if DEBUG: print(f"From {heaps}, push to losing situation {t}")
                WIN.add(heaps)
                return True
            else:
                if not (is_winning_situation(t)):
                    if DEBUG: print(f"From {heaps}, push to losing situation {t}")
                    WIN.add(heaps)
                    return True
    LOSE.add(heaps)
    return False

def simulate_multiple_heaps():
    for l in range(2, 6):
        for heaps in product([list(range(7))] * l):
            print(heaps)

simulate_multiple_heaps()

def solution():
    # code solution here
    pass

def main():
    t = read_int()

    for i in range(t):
        s = solution()
        print(f"Case #{ i + 1 }: {s}")

# if __name__ == "__main__":
#     main()
