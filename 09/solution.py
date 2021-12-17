# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201
# Run with pypy to make it faster!!!
from collections import defaultdict
# from rich import print

def read_int():
    return int(input())

def read_int_array():
    return [int(ss) for ss in input().split()]

def is_collision(s1, x1, y1, s2, x2, y2):
    x1min = x1
    x1max = x1 + len(s1[0]) - 1
    y1min = y1
    y1max = y1 + len(s1) - 1
    x2min = x2
    x2max = x2 + len(s2[0]) - 1
    y2min = y2
    y2max = y2 + len(s2) - 1

    if x2max < x1min or x2min > x1max:
        return False
    if y2max < y1min or y2min > y1max:
        return False

    for y, row in enumerate(s2):
        y2 = y + y2min
        y1 = y2 - y1min
        if y1 < 0 or y1 >= len(s1):
            continue
        for x, c in enumerate(row):
            if c == "0":
                continue
            x2 = x + x2min
            x1 = x2 - x1min
            if x1 < 0 or x1 >= len(s1[0]):
                continue
            if s1[y1][x1] == "1":
                return True
    return False

def solution(sprites, instances):
    collisions = set()
    n = len(instances)

    for i in range(n):
        for j in range(i + 1, n):
            sid1, x1, y1 = instances[i]
            sid2, x2, y2 = instances[j]
            s1 = sprites[sid1]
            s2 = sprites[sid2]
            if is_collision(s1, x1, y1, s2, x2, y2):
                collisions.add((i, j))
    return len(collisions)

def solution_slow(sprites, instances):
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
        # print(solution_slow(sprites, instances))

if __name__ == "__main__":
    main()
