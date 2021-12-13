# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201
from fractions import Fraction
from rich import print

def read_int():
    return int(input())

def read_int_array():
    return [int(ss) for ss in input().split()]

def parsekv(s, d1, d2):
    pairs = s.split(d1)
    scores = {}
    for p in pairs:
        k, v = p.split(d2)
        scores[k] = Fraction(v)
    return scores

def parsedict(s):
    s = s[1:-1]
    s = s.replace(" ", "")
    s = s.replace("'", "")
    return parsekv(s, ",", ":")

def parsetuples(s):
    s = s[1:-1]
    s = s.replace(" ", "")
    s = s.replace("'", "")
    s = s.replace("),", ";")
    s = s.replace("(", "")
    s = s.replace(")", "")
    return parsekv(s, ";", ",")

def parse_scores(s):
    if ":" in s:
        return parsedict(s)
    if "]" in s:
        return parsetuples(s)
    return parsekv(s, ",", "=")

def solution(test):
    words, scoretxt = test.split("|")
    left, right = words.split("-")
    scores = parse_scores(scoretxt)
    # print(left, right, scoretxt, scores)
    ls = sum([scores[l] for l in left])
    rs = sum([scores[r] for r in right])
    if ls == rs:
        return "-"
    elif ls > rs:
        return left
    return right

def main():
    t = read_int()

    for i in range(t):
        l = input().strip()
        s = solution(l)
        print(f"Case #{ i + 1 }: {s}")

if __name__ == "__main__":
    main()
