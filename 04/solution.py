# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201
# from rich import print
from itertools import product

def read_int():
    return int(input())

def read_int_array():
    return [int(ss) for ss in input().split()]

# D#E#F#G#A#BC#D#

# Line 1  [OK!]  Case #1: GABC#DEF#G
# Line 2  [OK!]  Case #2: ABbCDEbFGA
# Line 3  [OK!]  Case #3: ABC#DEF#GA
# Line 4 [WRONG] Case #4: BbCDEbFGAbBb
# Line 5  [OK!]  Case #5: D#E#F#G#A#BC#D#

NOTES = [
        ["A"],
        ["A#", "Bb"],
        ["B", "Cb"],
        ["B#", "C"],
        ["C#", "Db"],
        ["D"],
        ["D#", "Eb"],
        ["E"],
        ["E#", "F"],
        ["F#", "Gb"],
        ["G"],
        ["G#", "Ab"],
        ]

def isvalid(sol):
    for a, b in zip(sol, sol[1:]):
        if a[0] == b[0]:
            return False
    return True

def solution(note, seq):
    index = None
    for i, g in enumerate(NOTES):
        if note in g:
            index = i
            break
    ans = [[note]]
    for jump in seq:
        if jump == "T":
            index += 2
        else:
            index += 1
        if index >= len(NOTES):
            index = index % len(NOTES)
        ans.append(NOTES[index])

    finalsol = min(["".join(sol) for sol in product(*ans) if isvalid(sol)])

    return finalsol

def main():
    t = read_int()

    for i in range(t):
        note = input().strip()
        seq = input().strip()
        s = solution(note, seq)
        print(f"Case #{ i + 1 }: {s}")

def test():
    assert solution("G", "TTTsTTs") == "GABC#DEF#G"
    assert solution("A", "sTTsTTT") == "ABbCDEbFGA"
    assert solution("A", "TTsTTsT") == "ABC#DEF#GA"

if __name__ == "__main__":
    main()
    # test()
