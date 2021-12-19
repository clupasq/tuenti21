# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201
from math import log, floor
from rich import print
from itertools import product
from collections import Counter

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
        return heaps[0] % 3 > 0
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

    dim = 7
    k = 1
    l = 2
    m = 3
    n = 3
    print("  ", end="")
    for j in range(1, dim):
        print(f"  {j:2}  ", end="")
    print()
    for i in range(1, dim):

        print(f"{i:2} ", end="")
        for j in range(1, dim):
            result = is_winning_situation((i, j, k))
            result = "False " if not result else "True  "
            print(result, end="")
        print()

    # for l in range(2, 4):
    #     for heaps in product(*[list(range(1, 7))] * l):
    #         print(heaps, is_winning_situation(heaps))

# simulate_multiple_heaps()

# for i in [1,2,3]:
#     for j in range(1, 7):
#         t = tuple([i] * j)
#         print(t, is_winning_situation(t))

def other_random_tests():
    for t in [
            (1, 1, 3),
            (2, 2, 3),

            (1, 1, 2, 2, 3, 3, 3, 3),

            (1, 2),
            (1, 1, 1, 1, 2, 2, 2, 2, 2, 2),
            (1, 1, 2, 2, 3, 3),
            (1, 1, 1, 2, 2, 2, 3, 3, 3),
            # (1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3),

            (1, 1, 1, 1, 2, 2, 3, 3),

            (1, 1, 1),
            ]:
        print(t, is_winning_situation(t))
        print()

# Conclusion:
#   only the values %3 matter; no need to work with huge numbers.
#   WOW: heaps with %3==0 can be reoved and the result does not change!
#   OK, it seems that if the counts of ones and twos are *both* even, it's a losing situation.
#   Otherwise, it's a win


def mod3(x):
    """
    Avoid working with 0s; it messes with the log function
    """
    m = x % 3
    return 3 if m == 0 else m

def solution_old(xs):
    """
    This one passed the test input
    """
    xs = [mod3(x) for x in xs]
    is_winning = is_winning_situation(tuple(xs))
    return "Edu" if is_winning else "Alberto"

def solution(xs):
    xc = Counter([mod3(x) for x in xs])
    ones = xc[1]
    twos = xc[2]
    is_winning = ones % 2 > 0 or twos % 2 > 0
    return "Edu" if is_winning else "Alberto"

def main():
    t = read_int()

    for i in range(t):
        n = read_int()
        xs = read_int_array()
        s = solution(xs)
        print(f"Case #{ i + 1 }: {s}")

if __name__ == "__main__":
    main()
