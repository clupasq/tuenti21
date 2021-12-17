# pylint: disable=C0112,C0103,R0903,C0116,C0114,R0201

def read_int():
    return int(input())

def read_int_array():
    return [int(ss) for ss in input().split()]

def solution(n, k, words):
    return (n, k)

def main():
    t = read_int()

    for i in range(t):
        n, k = read_int_array()
        words = [input().strip() for _ in range(n)]
        s = solution(n, k, words)
        print(f"Case #{ i + 1 }: {s}")

if __name__ == "__main__":
    main()
