# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201
from rich import print
from collections import deque, defaultdict

def read_int():
    return int(input())

def read_int_array():
    return [int(ss) for ss in input().split()]

def can_reach_btc(coin, exchanges):
    seen = set()
    todo = deque([coin])
    while len(todo) > 0:
        crt = todo.popleft()
        if crt == "BTC":
            return True
        seen.add(crt)
        if crt not in exchanges:
            continue
        for cc in exchanges[crt]:
            if cc not in seen:
                todo.append(cc)
    return False

def find_deadends(exchanges):
    deadends = set()
    for c in exchanges:
        if c == "BTC":
            continue
        if not can_reach_btc(c, exchanges):
            deadends.add(c)
    return deadends

def solution(exchanges):
    deadends = find_deadends(exchanges)
    if all([q <= 1 for x in exchanges.values() for q in x.values()]):
        return 1
    best_by_coin = defaultdict(int)
    todo = deque([("BTC", 1)])

    while len(todo) > 0:
        coin, qty = todo.popleft()
        if best_by_coin[coin] >= qty:
            continue
        best_by_coin[coin] = qty
        if coin not in exchanges:
            continue
        if "BTC" in exchanges[coin]:
            q = exchanges[coin]["BTC"] * qty
            if q > 1:
                return q
        for other_coin, ex in exchanges[coin].items():
            if other_coin in deadends:
                continue
            qq = ex * qty
            if best_by_coin[qq] >= qq:
                continue
            todo.append((other_coin, qq))
    return 1

def main():
    t = read_int()

    for i in range(t):
        m = read_int()
        exchanges = {}
        for _ in range(m):
            count = int(input().strip().split(" ")[1])
            for _j in range(count):
                fromSymbol, qty, toSymbol = input().strip().split("-")
                qty = int(qty)
                if qty == 0:
                    continue
                if fromSymbol not in exchanges:
                    exchanges[fromSymbol] = {}
                avail = exchanges[fromSymbol]
                if toSymbol in avail and avail[toSymbol] > qty:
                    continue
                avail[toSymbol] = qty
        s = solution(exchanges)
        print(f"Case #{ i + 1 }: {s}")

if __name__ == "__main__":
    main()
