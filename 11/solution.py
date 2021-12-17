# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201
import math
import itertools
from rich import print
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Dict
from itertools import permutations
from random import randint, choice
from string import ascii_lowercase

def randomword():
    l = randint(5, 10)
    return "".join((choice(ascii_lowercase) for _ in range(l)))

def random_testcase():
    n, k = choice([
        [9, 3],
        [6, 2],
        [6, 3],
        [4, 2],
        [8, 4],
        ])
    words = [randomword() for _ in range(n)]
    return n, k, words

# Brute force shit
def bf_longest_prefix(words):
    i = -1
    while True:
        i += 1
        crtchar = None
        for w in words:
            if i >= len(w):
                return i
            if crtchar is None:
                crtchar = w[i]
            elif crtchar != w[i]:
                return i
    raise Exception("Whyyy???")

def bf(n, k, words):
    best = 0
    for p in permutations(words):
        score = 0
        for i in range(0, n, k):
            score += bf_longest_prefix(p[i:i+k])
        best = max(best, score)
    return best

@dataclass
class TrieNode:
    children: Dict[str, "TrieNode"] = field(default_factory=lambda: defaultdict(TrieNode))
    count: int = 0
    endcount: int = 0

    def add(self, word, i=0):
        self.count += 1
        if i == len(word):
            self.endcount += 1
        else:
            self.children[word[i]].add(word, i + 1)

    def bestscore(self, k, depth=0):
        if self.count < k:
            return 0, deque()
        best = depth
        best_suffix = deque()
        for l, c in self.children.items():
            bs, suff = c.bestscore(k, depth + 1)
            if bs > best:
                best = bs
                suff.appendleft(l)
                best_suffix = suff
        return best, best_suffix

    def shake_the_trie(self, k, prefix, i=0):
        if i < len(prefix):
            self.count -= k
            self.children[prefix[i]].shake_the_trie(k, prefix, i + 1)
        else:
            self.prune(k)

    def prune(self, k):
        can_remove = min(k, self.endcount)
        self.endcount -= can_remove
        self.count -= can_remove
        left = k - can_remove
        total_removed = can_remove
        if left == 0:
            return total_removed
        for l, c in self.children.items():
            removed_count = c.prune(left)
            total_removed += removed_count
            self.count -= removed_count
            left -= removed_count
            if left == 0:
                break
        return total_removed

def faster(n, k, words):
    trie = TrieNode()
    for w in words:
        trie.add(w)
    total_score = 0
    for _ in range(0, n, k):
        score, prefix = trie.bestscore(k)
        trie.shake_the_trie(k, prefix)
        total_score += score
    return total_score

##############
def test():
    assert bf_longest_prefix("abc abcd abbbb".split(" ")) == 2
    assert bf_longest_prefix("abc abc abcz".split(" ")) == 3
    assert bf_longest_prefix("longword".split(" ")) == 8

    assert 3 == bf(6, 3, ["getHeight", "pairs", "getWidth", "invert", "getDepth", "invoke"])
    assert 3 == faster(6, 3, ["getHeight", "pairs", "getWidth", "invert", "getDepth", "invoke"])

def perftest():
    for _ in range(10000):
        # assert 3 == bf(6, 3, ["getHeight", "pairs", "getWidth", "invert", "getDepth", "invoke"])
        assert 3 == faster(6, 3, ["getHeight", "pairs", "getWidth", "invert", "getDepth", "invoke"])

def random_correctness_tests():
    for _ in range(1000):
        testcase = random_testcase()
        print(".", end="")
        slowr = bf(*testcase)
        fastr = faster(*testcase)
        if slowr != fastr:
            print(testcase)
            print("slow ", slowr)
            print("fast ", fastr)
            raise Exception("Random test failed")

def run_tests():
    test()
    # perftest()
    random_correctness_tests()

# run_tests()

def read_int():
    return int(input())

def read_int_array():
    return [int(ss) for ss in input().split()]

def solution(n, k, words):
    return faster(n, k, words)

def main():
    t = read_int()

    for i in range(t):
        n, k = read_int_array()
        words = [input().strip() for _ in range(n)]
        s = solution(n, k, words)
        print(f"Case #{ i + 1 }: {s}")

if __name__ == "__main__":
    main()
