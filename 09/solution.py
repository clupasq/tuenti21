# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201
from collections import defaultdict
from rich import print

def read_int():
    return int(input())

def read_int_array():
    return [int(ss) for ss in input().split()]

def solution(sprites, instances):
    atcoords = defaultdict(set)
    collisions = set()

    for iid, (sid, posx, posy) in enumerate(instances):
        sprite = sprites[sid]
        for y, row in enumerate(sprite):
            for x, bit in enumerate(row):
                if bit == "0":
                    continue
                yy = posy + y
                xx = posx + x
                pos = (yy, xx)
                for other in atcoords[pos]:
                    coll = tuple(sorted([other, iid]))
                    collisions.add(coll)
                atcoords[pos].add(iid)
    return len(collisions)

def main():
    t = read_int()
    ns = read_int()
    sprites = []
    for _ in range(ns):
        w, h = read_int_array()
        sprites.append([input().strip() for y in range(h)])

    for i in range(t):
        instancecount = read_int()
        instances = []
        for _ in range(instancecount):
            instances.append(read_int_array())
        s = solution(sprites, instances)
        print(f"Case #{ i + 1 }: {s}")

if __name__ == "__main__":
    main()
