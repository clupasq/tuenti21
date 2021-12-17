from dataclasses import dataclass
from typing import List
import re
from rich import print

regex = r"^(\d+):(\d+):(\d+).(\d+) IP 127\.0\.0\.1 > 127\.0\.0\.1: ICMP echo request, id (\d+), seq (\d+), length (\d+)$"

records = []


@dataclass
class Record:
    h: int
    m: int
    s: int
    ms: int
    id: int
    seq: int
    length: int
    data: List[int]

    # Data:
    # 24 = all 0
    # 26 = all 0


def readhex(s):
    ans = []
    i = 0
    while i < len(s):
        if s[i] == " ":
            i += 1
            continue
        hd = s[i:i+2]
        ans.append(int(hd, 16))
        i += 2
    return ans

with open("./icmps.txt", "r") as f:
    ls = [l.strip() for l in f.readlines()]
    n = len(ls)
    for i in range(0, n, 3):
        l1 = ls[i]
        l2 = ls[i + 1]
        l3 = ls[i + 2]

        match = re.match(regex, l1)
        h, m, s, ms, id, seq, length = [int(g) for g in match.groups()]

        l2 = l2[9:48]
        l3 = l3[9:48]
        data = readhex(l2) + readhex(l3)
        record = Record(h, m, s, ms, id, seq, length, data)
        records.append(record)

for r in records:
    print(r.h, r.m, r.s, r.ms, r.id, r.seq, r.length)
    print(r.data[26])

uniq = set([tuple(r.data[24:25]) for r in records])
print(uniq)
print(len(uniq))


