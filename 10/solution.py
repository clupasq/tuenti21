from dataclasses import dataclass
from typing import List
import re
# from rich import print
import base64
import binascii

regex = r"^(\d+):(\d+):(\d+).(\d+) IP 127\.0\.0\.1 > 127\.0\.0\.1: ICMP echo request, id (\d+), seq (\d+), length (\d+)$"


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

def read_records(): # pylint: disable=too-many-locals
    rs = []

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
            rs.append(record)
    return rs

records = read_records()

# Data:
# 0 = all 69
# 1 = all 0
# 2 = all 0
# 3 = all 29
# 4 = all 0
# 5 = all 1
# 6 = all 0
# 7 = all 0
# 8 = all 64
# 9 = all 1
# 10 = all 124
# 11 = all 221
# 12 = all 127
# 13 = all 0
# 14 = all 0
# 15 = all 1
# 16 = all 127
# 17 = all 0
# 18 = all 0
# 19 = all 1
# 20 = all 8
# 21 = all 0
# 24 = all 0
# 26 = all 0
#
# 22 = min=2 max=255 distinct=109
# 23 = min=0 max=255 distinct=145
# 25 = min=32 max=121 distinct=22
#     -> What a mess, you will need to reorder everything to get the price x3
#     -> Also, equal to id.
# 27 = min=1 max=213 distinct=213 -> the seq value
# 28 = min=0 max=255 distinct=103

# print([r.data[25] for r in records])
# print("".join([chr(r.data[25]) for r in records]))
# for r in records:
#     print("\t".join(map(str, r.data)))

def hexi(vv):
    h = hex(vv)[2:]
    if len(h) == 1:
        h = "0" + h
    return h

# # IDEA: order by all columns and attempt base64 decode of hexs
# HEXS = [[hexi(v) for v in r.data] for r in records]
# # print(HEXS)
# for i in range(29):
#     for j in range(29):
#         vals = [r[i] for r in sorted(HEXS, key=lambda x:x[j])]
#         x = "".join(vals)
#         try:
#             print(base64.b64decode(x))
#         except binascii.Error:
#             pass

records = list(sorted(records, key=lambda x: x.seq))
for i in range(29):
    print("".join([chr(r.data[i]) for r in records]))
    print([(r.data[i]) for r in records])

# Damn! there's a PNG in there!

# for r1, r2 in zip(records, records[1:]):
#     if r1.seq > r2.seq:
#         print(r1, r2)

import struct
pngBytes = [r.data[28] for r in records]
with open("./secret.png", "wb") as pngf:
    pngf.write((''.join(chr(i) for i in pngBytes)).encode('charmap'))
